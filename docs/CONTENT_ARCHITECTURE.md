# Sanatan Gyan Content Architecture — v0.7

## 1. Offline knowledge corpus

`Resources/Raw/sanatan_content.json` contains the bilingual knowledge articles. Article content stays data-driven instead of being hard-coded into Razor pages.

The proof-focused sections follow a strict UI/content rule:

- `Verified Facts` => `Strong Evidence` + at least one traceable source.
- `Garv with Proof` => `Strong Evidence` + at least one traceable source.
- `Verified Science & Knowledge` => curated verified-fact slugs only.
- Weak evidence categories are not part of the packaged v0.7 corpus.

Traditional/philosophical articles remain available in their own educational categories without being shown with a scientific-proof badge.

## 2. Bilingual model

Articles independently store English/Hindi titles, summaries, bodies and sections. `LanguageService` switches the UI and article language locally. Official source publication titles remain unchanged so the references can be verified accurately.

## 3. Hindu Texts Library

`Resources/Raw/sanatan_texts.json` is a separate bilingual catalog of 136 Hindu textual works/families across 10 major groups. `ScriptureService` loads it offline and powers `/texts` and `/text/{slug}`.

The catalog is intentionally separate from the article corpus because future full scripture reading requires a deeper hierarchical model such as:

`KnowledgeWork -> ContentNode -> TextVariant -> Translation -> Commentary -> Source`.

## 4. Learning catalog

`Resources/Raw/sanatan_learning.json` stores six structured learning paths and six quizzes. v0.7 uses positive verified-fact/science paths instead of a viral-claim course.

`LearningProgressService` stores completed lessons and quiz scores locally with MAUI Preferences.

## 5. Daily Sanatan and Panchang

`DailySanatanService` chooses deterministic daily learning, verified fact and Pride with Proof cards from the packaged corpus.

`PanchangService` calculates an offline sunrise-based daily Panchang for a selected Indian city. It uses Astronomy Engine for astronomical positions/rise-set calculations and derives:

- Tithi/Paksha from Moon-Sun elongation
- Nakshatra from sidereal Moon longitude
- Yoga from sidereal Sun + Moon longitude
- Karana from half-tithi divisions
- Amanta-style Masa from consecutive new moons and sidereal solar rashi
- Ritu from lunar month grouping
- Vara, sunrise and sunset

The selected city is stored locally. No paid API or server is required.

## 6. Knowledge graph

`RelatedSlugs` plus category/tag fallback drive article connections and the `/graph/{slug}` view. No cloud graph database is required.

## 7. Future content delivery

MilesWeb can later host static signed/versioned content packages. The mobile app can compare a manifest version, download new knowledge/text catalog files, validate them, and swap the local content package while leaving user bookmarks and progress untouched.
