from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "SanatanGyan"
errors: list[str] = []
passes: list[str] = []


def ok(message: str) -> None: passes.append(message)
def fail(message: str) -> None: errors.append(message)

# Core knowledge corpus
content_path = PROJECT / "Resources" / "Raw" / "sanatan_content.json"
try:
    items = json.loads(content_path.read_text(encoding="utf-8"))
    ok(f"Knowledge corpus parses ({len(items)} entries)")
except Exception as exc:
    items = []
    fail(f"Knowledge corpus parse failed: {exc}")

if items:
    ids = [str(x.get("id", "")) for x in items]
    slugs = [str(x.get("slug", "")) for x in items]
    if len(ids) == len(set(x.lower() for x in ids)) and all(ids): ok("Knowledge ids are unique")
    else: fail("Knowledge ids are missing or duplicated")
    if len(slugs) == len(set(x.lower() for x in slugs)) and all(slugs): ok("Knowledge slugs are unique")
    else: fail("Knowledge slugs are missing or duplicated")

    required_bilingual = ["titleEn", "titleHi", "summaryEn", "summaryHi"]
    missing_bilingual = [(x.get("slug"), f) for x in items for f in required_bilingual if not str(x.get(f, "")).strip()]
    if missing_bilingual: fail(f"Knowledge bilingual fields missing: {missing_bilingual[:10]}")
    else: ok("Knowledge entries have complete English/Hindi core text")

    known = {x.lower() for x in slugs}
    broken = [(x.get("slug"), r) for x in items for r in x.get("relatedSlugs", []) if r.lower() not in known]
    if broken: fail(f"Broken related links: {broken[:10]}")
    else: ok("Knowledge graph article references resolve")

    bad_urls = [(x.get("slug"), s.get("url")) for x in items for s in x.get("sources", []) if s.get("url") and not str(s.get("url")).startswith(("https://", "http://"))]
    if bad_urls: fail(f"Invalid source URLs: {bad_urls[:10]}")
    else: ok("All external source URLs use HTTP/HTTPS")

    cats = Counter(x.get("category", "") for x in items)
    if "Claim Checker" in cats or "Science & Research" in cats:
        fail("Legacy Claim Checker / weak Science category still exists")
    else:
        ok("Legacy Claim Checker and mixed-evidence Science categories removed")

    weak = [x.get("slug") for x in items if x.get("evidenceLevel") in {"Moderate Evidence", "Preliminary Evidence", "Unsupported"}]
    if weak: fail(f"Weak/unsupported evidence entries remain: {weak[:10]}")
    else: ok("No Moderate, Preliminary or Unsupported evidence entries remain")

    for category in ["Verified Facts", "Garv with Proof", "Epic Evidence"]:
        subset = [x for x in items if x.get("category") == category]
        invalid = [x.get("slug") for x in subset if x.get("evidenceLevel") != "Strong Evidence" or not x.get("sources")]
        if not subset: fail(f"{category} is empty")
        elif invalid: fail(f"{category} contains non-verified entries: {invalid[:10]}")
        else: ok(f"{category} is strict verified-only ({len(subset)} entries)")
else:
    cats = Counter()

# v0.7 quality and epic-history checks
if items:
    if len(items) >= 230: ok(f"v0.7 knowledge scope expanded ({len(items)} entries)")
    else: fail("v0.7 knowledge corpus is smaller than expected")
    sacred_required={"traditional-ramayana-era","traditional-mahabharata-era"}
    if sacred_required.issubset({x.get("slug") for x in items}): ok("Ramayana and Shri Krishna–Mahabharata sacred eras are present")
    else: fail("Sacred Ramayana/Mahabharata timeline entries missing")
    epic=[x for x in items if x.get("category")=="Epic Evidence"]
    if len(epic)>=12 and all(x.get("evidenceLevel")=="Strong Evidence" and x.get("sources") for x in epic): ok(f"Epic Evidence hub is strict source-backed ({len(epic)} entries)")
    else: fail("Epic Evidence hub coverage or source policy failed")
    # Repeated boilerplate was a visible v0.6 problem; exact section bodies must now be unique across articles.
    for fld in ["contentEn","contentHi"]:
        bodies=[" ".join(str(s.get(fld,"")).split()).strip().lower() for x in items for s in x.get("sections",[]) if str(s.get(fld,"")).strip()]
        dup=[v for v,n in Counter(bodies).items() if n>1]
        if dup: fail(f"Repeated article section copy remains in {fld}: {len(dup)} duplicate blocks")
        else: ok(f"No repeated article section copy in {fld}")

# v0.8.1 content quality
latin_hi = re.compile(r"[A-Za-z]{2,}")
if items:
    short_body=[x.get("slug") for x in items if len((x.get("bodyHi") or "").strip()) < 240 or len((x.get("bodyEn") or "").strip()) < 260]
    if short_body: fail(f"Knowledge pages with short detailed body remain: {len(short_body)}")
    else: ok("All knowledge pages have substantial bilingual detail bodies")
    short_sections=[x.get("slug") for x in items if len(x.get("sections",[])) < 3]
    if short_sections: fail(f"Knowledge pages with fewer than 3 explanatory sections: {len(short_sections)}")
    else: ok("All knowledge pages have at least three explanatory sections")
    mixed=[]
    for x in items:
        vals=[x.get("titleHi",""),x.get("summaryHi",""),x.get("bodyHi","")]
        for s in x.get("sections",[]): vals += [s.get("titleHi",""),s.get("contentHi","")]
        if any(latin_hi.search(v or "") for v in vals): mixed.append(x.get("slug"))
    if mixed: fail(f"Roman-English/Hinglish remains in Hindi knowledge content: {len(mixed)}")
    else: ok("Hindi knowledge content is Devanagari-only in core article fields")

# Hindu texts catalog
texts_path = PROJECT / "Resources" / "Raw" / "sanatan_texts.json"
try:
    texts = json.loads(texts_path.read_text(encoding="utf-8"))
    ok(f"Hindu texts catalog parses ({len(texts)} entries)")
    if len(texts) < 120: fail("Hindu texts catalog is smaller than expected")
    if all(str(x.get("archiveUrl","")).startswith("https://archive.org/") for x in texts): ok("Every Hindu text page has an Internet Archive public-edition link")
    else: fail("One or more Hindu text entries are missing the Internet Archive link")
    direct_count=sum(1 for x in texts if str(x.get("readOnlineUrl","")).startswith(("http://","https://")))
    if direct_count >= 12: ok(f"Curated direct read-online links present for major texts ({direct_count})")
    else: fail(f"Too few curated direct read-online links ({direct_count})")
    required = ["slug", "titleEn", "titleHi", "category", "categoryHi", "kindEn", "kindHi", "descriptionEn", "descriptionHi", "languageEn", "languageHi", "keyThemesEn", "keyThemesHi", "structureEn", "structureHi", "whyReadEn", "whyReadHi", "studyNoteEn", "studyNoteHi"]
    missing = [(x.get("slug"), f) for x in texts for f in required if not str(x.get(f, "")).strip()]
    if missing: fail(f"Texts catalog missing bilingual metadata: {missing[:10]}")
    else: ok("Hindu texts catalog has complete bilingual metadata")
    tslugs = [x["slug"].lower() for x in texts]
    if len(tslugs) == len(set(tslugs)): ok("Hindu texts catalog slugs are unique")
    else: fail("Duplicate Hindu text slug found")
    if len(set(x["category"] for x in texts)) >= 10: ok("Hindu texts catalog spans 10+ major textual families")
    else: fail("Hindu texts catalog category coverage is too small")
    text_short=[x.get("slug") for x in texts if len((x.get("keyThemesHi") or "")) < 180 or len((x.get("whyReadHi") or "")) < 150 or len((x.get("studyNoteHi") or "")) < 170]
    if text_short: fail(f"Hindu text pages still too brief: {len(text_short)}")
    else: ok("All Hindu text pages have expanded Hindi study content")
    text_mixed=[]
    for x in texts:
        vals=[x.get("descriptionHi",""),x.get("keyThemesHi",""),x.get("whyReadHi",""),x.get("structureHi",""),x.get("studyNoteHi",""),x.get("archiveLabelHi",""),x.get("readOnlineLabelHi","")]
        if any(latin_hi.search(v or "") for v in vals): text_mixed.append(x.get("slug"))
    if text_mixed: fail(f"Roman-English remains in Hindi Hindu-text prose: {len(text_mixed)}")
    else: ok("Hindi Hindu-text prose is free of Roman-English mixing")
except Exception as exc:
    texts = []
    fail(f"Hindu texts catalog parse failed: {exc}")

# Learning catalog
learning_path = PROJECT / "Resources" / "Raw" / "sanatan_learning.json"
try:
    learning = json.loads(learning_path.read_text(encoding="utf-8"))
    paths = learning.get("paths", [])
    quizzes = learning.get("quizzes", [])
    known = {x.get("slug", "").lower() for x in items}
    broken = [(p.get("id"), s) for p in paths for s in p.get("lessonSlugs", []) if s.lower() not in known]
    broken += [(q.get("id"), qq.get("relatedSlug")) for q in quizzes for qq in q.get("questions", []) if qq.get("relatedSlug") and qq.get("relatedSlug").lower() not in known]
    if broken: fail(f"Learning references missing articles: {broken[:10]}")
    else: ok("Learning paths/quizzes resolve to current knowledge articles")
    qcount = sum(len(q.get("questions", [])) for q in quizzes)
    if len(paths) >= 6 and qcount >= 30: ok(f"Structured learning present ({len(paths)} paths / {qcount} questions)")
    else: fail("Learning scope is below expected size")
    titles = " ".join(str(p.get("titleEn", "")) for p in paths).lower()
    if "viral claim" in titles or "fact, tradition or viral" in titles: fail("Legacy viral-claim course still visible")
    else: ok("Learning paths use positive verified-facts framing")
except Exception as exc:
    fail(f"Learning catalog parse failed: {exc}")

# XML/project config
xml_files = [
    PROJECT / "SanatanGyan.csproj", PROJECT / "App.xaml", PROJECT / "MainPage.xaml",
    PROJECT / "Platforms" / "Android" / "AndroidManifest.xml",
    PROJECT / "Platforms" / "Windows" / "App.xaml",
    PROJECT / "Platforms" / "Windows" / "Package.appxmanifest",
    PROJECT / "Platforms" / "Windows" / "app.manifest",
]
for path in xml_files:
    try: ET.parse(path); ok(f"XML parses: {path.relative_to(ROOT)}")
    except Exception as exc: fail(f"XML failed: {path.relative_to(ROOT)}: {exc}")

csproj = (PROJECT / "SanatanGyan.csproj").read_text(encoding="utf-8")
if "<TargetFrameworks>net10.0-android;net10.0-windows10.0.19041.0</TargetFrameworks>" in csproj:
    ok("Both Android and Windows target frameworks are declared unconditionally")
else:
    fail("TargetFrameworks must unconditionally include both Android and Windows")
checks = [
    ("net10.0-android" in csproj and "net10.0-windows10.0.19041.0" in csproj, "Android and Windows targets configured"),
    ("<WindowsPackageType>None</WindowsPackageType>" in csproj, "Visual Studio Windows debug is unpackaged"),
    ("<UseMonoRuntime>false</UseMonoRuntime>" in csproj, "Windows uses CoreCLR rather than Mono"),
    ("<WindowsAppSDKSelfContained>true</WindowsAppSDKSelfContained>" in csproj, "Visual Studio F5 bundles the Windows App SDK runtime"),
    ("<RuntimeIdentifier>" not in csproj, "Normal Windows restore/build does not force a RuntimeIdentifier"),
    ("<AndroidManifest>" not in csproj, "Android manifest override removed; MAUI uses the standard Platforms/Android manifest"),
    ('<MauiIcon Include="Resources/AppIcon/appicon.png" />' in csproj, "PNG launcher icon configured"),
    ('<MauiSplashScreen Include="Resources/Splash/splash.png"' in csproj, "Matching splash artwork configured"),
    ("<ApplicationDisplayVersion>0.8.1</ApplicationDisplayVersion>" in csproj and "<ApplicationVersion>15</ApplicationVersion>" in csproj, "Application version is 0.8.1 / build 15"),
    ("CosineKitty.AstronomyEngine" in csproj and 'Version="2.1.19"' in csproj, "Offline astronomy dependency configured"),
]
for state, message in checks: ok(message) if state else fail(message)

# DI + core files
maui = (PROJECT / "MauiProgram.cs").read_text(encoding="utf-8")
for svc in ["KnowledgeService", "LanguageService", "DailySanatanService", "ScriptureService", "PanchangService"]:
    if f"AddSingleton<{svc}>" in maui: ok(f"{svc} registered")
    else: fail(f"{svc} not registered")

core_files = [
    PROJECT / "Services" / "PanchangService.cs", PROJECT / "Services" / "ScriptureService.cs",
    PROJECT / "Models" / "PanchangModels.cs", PROJECT / "Models" / "ScriptureInfo.cs",
    PROJECT / "Components" / "PanchangTile.razor", PROJECT / "Components" / "Pages" / "Today.razor",
    PROJECT / "Components" / "Pages" / "Texts.razor", PROJECT / "Components" / "Pages" / "TextDetail.razor",
    PROJECT / "Components" / "Pages" / "Science.razor", PROJECT / "Components" / "Pages" / "ClaimChecker.razor",
    PROJECT / "Components" / "Pages" / "EpicEvidence.razor", PROJECT / "Components" / "Pages" / "Timeline.razor",
    ROOT / "Build-APK.bat", ROOT / "Run-Windows.bat", ROOT / "THIRD_PARTY_NOTICES.md",
]
missing = [str(x.relative_to(ROOT)) for x in core_files if not x.exists()]
if missing: fail(f"Core v0.7 files missing: {missing}")
else: ok("Core v0.7 files present")

# UI safety/strict evidence checks
science = (PROJECT / "Components" / "Pages" / "Science.razor").read_text(encoding="utf-8")
facts = (PROJECT / "Components" / "Pages" / "ClaimChecker.razor").read_text(encoding="utf-8")
pride = (PROJECT / "Components" / "Pages" / "Pride.razor").read_text(encoding="utf-8")
card = (PROJECT / "Components" / "KnowledgeCard.razor").read_text(encoding="utf-8")
if all("Strong Evidence" in t and "Sources.Count > 0" in t for t in [science, facts, pride]): ok("Facts, verified science and Pride pages enforce strong sources")
else: fail("A proof-focused page does not enforce Strong Evidence + sources")
if "IsVerified(Item)" in card and "Moderate Evidence" not in card and "Unsupported" not in card: ok("Knowledge cards display only the verified proof badge")
else: fail("Knowledge card still exposes weak evidence badges")


# TextDetail regression check: v0.7 originally referenced `text` in markup without declaring/loading it.
text_detail = (PROJECT / "Components" / "Pages" / "TextDetail.razor").read_text(encoding="utf-8")
textdetail_tokens = [
    '[Parameter] public string Slug',
    'private ScriptureInfo? text',
    'OnParametersSetAsync()',
    'Scriptures.GetBySlugAsync(Slug)'
]
if all(token in text_detail for token in textdetail_tokens):
    ok("TextDetail declares and loads its scripture state (CS0103 regression covered)")
else:
    fail("TextDetail is missing route/state/loading code required by its markup")

# Header branding regression check.
layout = (PROJECT / "Components" / "Layout" / "MainLayout.razor").read_text(encoding="utf-8")
css = (PROJECT / "wwwroot" / "css" / "app.css").read_text(encoding="utf-8")
if all(token in layout for token in ["ॐ", "SANATAN GYAN", "सनातन ज्ञान"]) and "sanatan-wordmark" in css:
    ok("Saffron/gold Om + Sanatan Gyan wordmark is present")
else:
    fail("Updated Sanatan wordmark is missing")

# Panchang UI/service checks
panchang_service = (PROJECT / "Services" / "PanchangService.cs").read_text(encoding="utf-8")
today = (PROJECT / "Components" / "Pages" / "Today.razor").read_text(encoding="utf-8")
required_panchang_tokens = ["MoonPhase", "SearchRiseSet", "Nakshatra", "Karana", "LahiriAyanamsa", "CalculateMasa"]
if all(t in panchang_service for t in required_panchang_tokens): ok("Offline Panchang engine includes Tithi/Paksha/Nakshatra/Yoga/Karana/Masa calculations")
else: fail("Offline Panchang engine is incomplete")
if all(t in today for t in ["panchang.Tithi", "panchang.Paksha", "panchang.Nakshatra", "panchang.Yoga", "panchang.Karana", "panchang.Masa", "panchang.SunriseLocal", "panchang.SunsetLocal"]): ok("Today page displays full daily Panchang summary")
else: fail("Today page does not display expected Panchang values")
if "Panchang.Locations" in today and "OnLocationChanged" in today: ok("Panchang supports selectable Indian city location")
else: fail("Panchang city selector missing")

# Visual Studio and APK helpers
try:
    launch = json.loads((PROJECT / "Properties" / "launchSettings.json").read_text(encoding="utf-8"))
    if launch["profiles"]["Windows Machine"]["commandName"] == "Project": ok("Visual Studio Windows Machine launch profile uses unpackaged Project mode")
    else: fail("Visual Studio Windows launch profile is not unpackaged Project mode")
except Exception as exc: fail(f"launchSettings.json invalid: {exc}")

apk = (ROOT / "Build-APK.bat").read_text(encoding="utf-8", errors="replace")
if all(t in apk for t in ["net10.0-android", "SignAndroidPackage", "AndroidPackageFormats=apk", "SanatanGyan-v0.8.1-LocalTest.apk", "dotnet restore \"%PROJECT%\""]): ok("One-click APK BAT targets v0.8.1, does a full restore, and uses SignAndroidPackage")
else: fail("APK BAT version/config not updated")

# Route and C# delimiter sanity
routes: list[tuple[str,str]] = []
for razor in PROJECT.rglob("*.razor"):
    text = razor.read_text(encoding="utf-8")
    routes += [(m.group(1).lower(), str(razor.relative_to(ROOT))) for m in re.finditer(r'@page\s+"([^"]+)"', text)]
route_names = [x[0] for x in routes]
if len(route_names) == len(set(route_names)): ok(f"Razor routes unique ({len(routes)})")
else: fail("Duplicate Razor route found")

collisions=[]
for razor in PROJECT.rglob("*.razor"):
    stem=razor.stem
    text=razor.read_text(encoding="utf-8")
    if re.search(rf'\b(?:private|protected|public|internal)\s+(?:async\s+)?(?:Task(?:<[^>]+>)?|void|bool|string|int)\s+{re.escape(stem)}\s*\(', text):
        collisions.append(str(razor.relative_to(ROOT)))
if collisions: fail(f"Razor class/member collisions: {collisions}")
else: ok("No Razor page/member name collisions detected")

brace_bad=[]
for cs in PROJECT.rglob("*.cs"):
    text=cs.read_text(encoding="utf-8")
    if text.count("{") != text.count("}"): brace_bad.append(str(cs.relative_to(ROOT)))
if brace_bad: fail(f"C# brace mismatch: {brace_bad}")
else: ok("C# brace-count sanity")

# v0.7.6 build regression checks
csproj_text = (PROJECT / "SanatanGyan.csproj").read_text(encoding="utf-8")
apk_bat_text = (ROOT / "Build-APK.bat").read_text(encoding="utf-8")
launch_text = (PROJECT / "Properties" / "launchSettings.json").read_text(encoding="utf-8")
root_manifest = PROJECT / "Platforms" / "Android" / "AndroidManifest.xml"
if root_manifest.exists() and 'package="com.arpit.sanatangyan"' in root_manifest.read_text(encoding="utf-8"):
    ok("Platforms/Android manifest exists with application package id")
else:
    fail("Platforms/Android manifest missing or package id not configured")
if "<WindowsPackageType>None</WindowsPackageType>" in csproj_text and '"commandName": "Project"' in launch_text:
    ok("Windows F5 uses unpackaged Project mode and does not require MSIX deployment")
else:
    fail("Windows unpackaged Visual Studio configuration regression")
if all(token in csproj_text for token in ["<WindowsAppSDKSelfContained>true</WindowsAppSDKSelfContained>", "<WindowsAppSdkDeploymentManagerInitialize>false</WindowsAppSdkDeploymentManagerInitialize>", "<PlatformTarget>x64</PlatformTarget>"]):
    ok("Windows local F5 bundles Windows App SDK and targets x64")
else:
    fail("Windows self-contained x64 configuration incomplete")
if "<AndroidManifest>" not in csproj_text:
    ok("No custom AndroidManifest MSBuild property; MAUI uses Platforms/Android/AndroidManifest.xml")
else:
    fail("Custom AndroidManifest property still present and can trigger XA1018")
if "-p:TargetFramework=%TFM%" in apk_bat_text or "-p:TargetFramework=net10.0-android" in apk_bat_text:
    fail("APK BAT still performs a target-specific restore that can break Windows project.assets.json")
else:
    ok("APK BAT does not clobber project.assets.json with an Android-only restore")
if all(token in apk_bat_text for token in ["SignAndroidPackage", "AndroidPackageFormats=apk", "AndroidKeyStore=false", "AndroidUseApkSigner=true"]):
    ok("APK BAT creates and signs a local-test APK using the official Android target")
else:
    fail("APK BAT signed-package command is incomplete")
if (ROOT / "Build-APK-Command.txt").exists(): ok("Copy-paste APK command file included")
else: fail("Build-APK-Command.txt missing")
if not (ROOT / "global.json").exists(): ok("No SDK feature-band pin; Visual Studio may use its installed .NET 10 workload")
else: fail("global.json still pins an SDK feature band")
if 'Version="$(MauiVersion)"' in csproj_text and csproj_text.count('Version="$(MauiVersion)"') >= 2:
    ok("MAUI package references follow the installed workload version")
else:
    fail("MAUI package references are still hard-pinned")
if (PROJECT / "Resources" / "AppIcon" / "appicon.png").exists(): ok("Om + SANATAN GYAN launcher PNG exists")
else: fail("Launcher PNG missing")
if (PROJECT / "Resources" / "Splash" / "splash.png").exists(): ok("Matching branded splash PNG exists")
else: fail("Branded splash PNG missing")
layout_text = (PROJECT / "Components" / "Layout" / "MainLayout.razor").read_text(encoding="utf-8")
if layout_text.count('class="nav-icon') >= 5 and all(x in layout_text for x in ['href="/learn"','href="/explore"','href="/search"','href="/saved"']):
    ok("Bottom navigation uses five custom vector icons")
else:
    fail("Bottom navigation vector icon refresh missing")


# v0.8 understanding + mobile safe-area
understanding=[x for x in items if x.get("category")=="Sanatan Understanding"] if items else []
if len(understanding) >= 40: ok(f"Respectful Sanatan Understanding library present ({len(understanding)} topics)")
else: fail("Sanatan Understanding library is incomplete")
css=(PROJECT / "wwwroot" / "css" / "app.css").read_text(encoding="utf-8")
index=(PROJECT / "wwwroot" / "index.html").read_text(encoding="utf-8")
mainactivity=(PROJECT / "Platforms" / "Android" / "MainActivity.cs").read_text(encoding="utf-8")
if "safe-area-inset-top" in css and "viewport-fit=cover" in index and "SetDecorFitsSystemWindows" in mainactivity:
    ok("Android status-bar / notch safe-area handling configured")
else:
    fail("Android safe-area handling is incomplete")
textdetail=(PROJECT / "Components" / "Pages" / "TextDetail.razor").read_text(encoding="utf-8")
if "ReadOnlineUrl" in textdetail and "ArchiveUrl" in textdetail and "Browser.OpenAsync" in textdetail:
    ok("Scripture detail page opens external public editions in the system browser")
else:
    fail("Scripture external-reading UI is incomplete")

print("Sanatan Gyan v0.8.1 static validation")
print("="*58)
for x in passes: print("[PASS]", x)
for x in errors: print("[FAIL]", x)
print("-"*58)
if cats:
    print("Knowledge corpus by category:")
    for name,count in sorted(cats.items()): print(f"  {name}: {count}")
if texts:
    print(f"Hindu texts catalog: {len(texts)} entries / {len(set(x['category'] for x in texts))} families")
print("-"*58)
print(f"PASS: {len(passes)}  FAIL: {len(errors)}")
sys.exit(1 if errors else 0)
