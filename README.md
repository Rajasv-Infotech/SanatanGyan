# Sanatan Gyan v0.8.1

.NET 10 MAUI Blazor Hybrid app targeting Android and Windows.

## Critical build fixes in v0.8.1

### Visual Studio Windows Machine / NETSDK1005
The project now declares both target frameworks in one unconditional property:

`net10.0-android;net10.0-windows10.0.19041.0`

This prevents `obj/project.assets.json` from being restored with Android only and then failing Windows F5 with `NETSDK1005`.

Also, all helper build commands now perform a **full project restore**. They do not run a target-specific restore that can overwrite `project.assets.json` with only one framework.

Expected fresh-extract workflow:

1. Extract the ZIP to a new folder.
2. Open `SanatanGyan.sln`.
3. Wait for Visual Studio/NuGet restore to complete.
4. Select `Debug | x64 | Windows Machine`.
5. Press F5.

`Run-Windows.bat` is optional only; it is not required before Visual Studio F5.

### Android XA1018 AndroidManifest path
The custom `<AndroidManifest>` MSBuild property has been completely removed.

.NET MAUI single-project automatically uses:

`SanatanGyan/Platforms/Android/AndroidManifest.xml`

No script or command passes a custom manifest path.

### APK build
`Build-APK.bat` does a full multi-target restore first, then builds only Android with `SignAndroidPackage`.

Output copied to:

`artifacts/android/SanatanGyan-v0.8.1-LocalTest.apk`

Equivalent commands are in `Build-APK-Command.txt`.

## Requirements

- Windows 10/11 x64
- Visual Studio 2022 with .NET MAUI workload
- .NET 10 SDK
- Android SDK/JDK installed by Visual Studio/MAUI workload

## If Visual Studio opened an older extracted version before

Do not overwrite an old v0.7.x directory. Extract v0.8.1 into a fresh folder. If needed, close Visual Studio and remove `.vs`, `SanatanGyan/bin`, and `SanatanGyan/obj`, then reopen the solution and allow restore to finish.


## v0.8.1 content quality upgrade
- All 276 knowledge pages now have a substantial bilingual body plus at least three explanatory sections.
- Hindi article content was cleaned so core Hindi fields no longer fall back to Roman-English/Hinglish wording.
- English article content remains fully English.
- Common repeated filler sections were replaced with category-aware explanations for philosophy, history, practices, deities, Indian knowledge systems, verified facts, epic evidence and Sanatan Understanding.
- High-visibility source-backed topics such as TKDL, Aryabhata and Sushruta received additional curated explanations.
- All 136 Hindu text pages now have longer descriptions, themes, structure, reading importance and study guidance in both Hindi and English.
- Hindi text-catalog prose uses Devanagari terminology (for example ऋग्वेद, यजुर्वेद and इंटरनेट आर्काइव) instead of mixed Roman wording.

## v0.8.1
- Mobile safe-area and Android status-bar handling improved for edge-to-edge Android devices.
- Added **Sanatan ko Samjhein / Understand Sanatan** with 45 respectful bilingual explanations of commonly misunderstood ideas, symbols and practices.
- The Hindu Texts Library now gives every one of its 136 catalog entries an external public-edition link (Internet Archive search scoped to that title).
- Major texts including Rigveda, Yajurveda, Atharvaveda, Valmiki Ramayana, Mahabharata, Bhagavad Gita, principal Upanishad collections and Patanjali Yoga Sutras also have curated read-online links to public-domain repositories.
- Text detail pages clearly distinguish the app's introduction from external editions/translations.
- Existing Windows/Android build fixes from v0.7.6 are retained: dual target restore, no custom AndroidManifest override, unpackaged Windows F5 configuration.
