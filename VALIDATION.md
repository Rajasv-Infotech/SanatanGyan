# Sanatan Gyan v0.8.1 Validation

## Result

**81 PASS / 0 FAIL**

## Content quality changes validated

- 276 bilingual knowledge pages parse successfully.
- Every knowledge page has a substantial Hindi and English detail body.
- Every knowledge page has at least three explanatory sections.
- No repeated article-section copy remains in Hindi or English.
- Core Hindi article fields contain no Roman-English/Hinglish wording.
- 136 Hindu text pages have expanded bilingual descriptions, themes, structure, study importance and reading guidance.
- Hindi Hindu-text prose is free of Roman-English mixing in the main content fields.
- Existing strict verified-fact/source rules remain intact.
- Existing Windows/Android project configuration checks remain green.

## Static validation log

```text
Sanatan Gyan v0.8.1 static validation
==========================================================
[PASS] Knowledge corpus parses (276 entries)
[PASS] Knowledge ids are unique
[PASS] Knowledge slugs are unique
[PASS] Knowledge entries have complete English/Hindi core text
[PASS] Knowledge graph article references resolve
[PASS] All external source URLs use HTTP/HTTPS
[PASS] Legacy Claim Checker and mixed-evidence Science categories removed
[PASS] No Moderate, Preliminary or Unsupported evidence entries remain
[PASS] Verified Facts is strict verified-only (15 entries)
[PASS] Garv with Proof is strict verified-only (8 entries)
[PASS] Epic Evidence is strict verified-only (13 entries)
[PASS] v0.7 knowledge scope expanded (276 entries)
[PASS] Ramayana and Shri Krishna–Mahabharata sacred eras are present
[PASS] Epic Evidence hub is strict source-backed (13 entries)
[PASS] No repeated article section copy in contentEn
[PASS] No repeated article section copy in contentHi
[PASS] All knowledge pages have substantial bilingual detail bodies
[PASS] All knowledge pages have at least three explanatory sections
[PASS] Hindi knowledge content is Devanagari-only in core article fields
[PASS] Hindu texts catalog parses (136 entries)
[PASS] Every Hindu text page has an Internet Archive public-edition link
[PASS] Curated direct read-online links present for major texts (15)
[PASS] Hindu texts catalog has complete bilingual metadata
[PASS] Hindu texts catalog slugs are unique
[PASS] Hindu texts catalog spans 10+ major textual families
[PASS] All Hindu text pages have expanded Hindi study content
[PASS] Hindi Hindu-text prose is free of Roman-English mixing
[PASS] Learning paths/quizzes resolve to current knowledge articles
[PASS] Structured learning present (6 paths / 30 questions)
[PASS] Learning paths use positive verified-facts framing
[PASS] XML parses: SanatanGyan/SanatanGyan.csproj
[PASS] XML parses: SanatanGyan/App.xaml
[PASS] XML parses: SanatanGyan/MainPage.xaml
[PASS] XML parses: SanatanGyan/Platforms/Android/AndroidManifest.xml
[PASS] XML parses: SanatanGyan/Platforms/Windows/App.xaml
[PASS] XML parses: SanatanGyan/Platforms/Windows/Package.appxmanifest
[PASS] XML parses: SanatanGyan/Platforms/Windows/app.manifest
[PASS] Both Android and Windows target frameworks are declared unconditionally
[PASS] Android and Windows targets configured
[PASS] Visual Studio Windows debug is unpackaged
[PASS] Windows uses CoreCLR rather than Mono
[PASS] Visual Studio F5 bundles the Windows App SDK runtime
[PASS] Normal Windows restore/build does not force a RuntimeIdentifier
[PASS] Android manifest override removed; MAUI uses the standard Platforms/Android manifest
[PASS] PNG launcher icon configured
[PASS] Matching splash artwork configured
[PASS] Application version is 0.8.1 / build 15
[PASS] Offline astronomy dependency configured
[PASS] KnowledgeService registered
[PASS] LanguageService registered
[PASS] DailySanatanService registered
[PASS] ScriptureService registered
[PASS] PanchangService registered
[PASS] Core v0.7 files present
[PASS] Facts, verified science and Pride pages enforce strong sources
[PASS] Knowledge cards display only the verified proof badge
[PASS] TextDetail declares and loads its scripture state (CS0103 regression covered)
[PASS] Saffron/gold Om + Sanatan Gyan wordmark is present
[PASS] Offline Panchang engine includes Tithi/Paksha/Nakshatra/Yoga/Karana/Masa calculations
[PASS] Today page displays full daily Panchang summary
[PASS] Panchang supports selectable Indian city location
[PASS] Visual Studio Windows Machine launch profile uses unpackaged Project mode
[PASS] One-click APK BAT targets v0.8.1, does a full restore, and uses SignAndroidPackage
[PASS] Razor routes unique (19)
[PASS] No Razor page/member name collisions detected
[PASS] C# brace-count sanity
[PASS] Platforms/Android manifest exists with application package id
[PASS] Windows F5 uses unpackaged Project mode and does not require MSIX deployment
[PASS] Windows local F5 bundles Windows App SDK and targets x64
[PASS] No custom AndroidManifest MSBuild property; MAUI uses Platforms/Android/AndroidManifest.xml
[PASS] APK BAT does not clobber project.assets.json with an Android-only restore
[PASS] APK BAT creates and signs a local-test APK using the official Android target
[PASS] Copy-paste APK command file included
[PASS] No SDK feature-band pin; Visual Studio may use its installed .NET 10 workload
[PASS] MAUI package references follow the installed workload version
[PASS] Om + SANATAN GYAN launcher PNG exists
[PASS] Matching branded splash PNG exists
[PASS] Bottom navigation uses five custom vector icons
[PASS] Respectful Sanatan Understanding library present (45 topics)
[PASS] Android status-bar / notch safe-area handling configured
[PASS] Scripture detail page opens external public editions in the system browser
----------------------------------------------------------
Knowledge corpus by category:
  Deities: 17
  Epic Evidence: 13
  Garv with Proof: 8
  History: 21
  Indian Knowledge Systems: 42
  Philosophy: 25
  Practices & Symbols: 29
  Sanatan Basics: 40
  Sanatan Understanding: 45
  Thinkers & Acharyas: 21
  Verified Facts: 15
Hindu texts catalog: 136 entries / 10 families
----------------------------------------------------------
PASS: 81  FAIL: 0
```
