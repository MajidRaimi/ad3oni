# Ad3oni — Flutter App Architecture & Conventions

Ad3oni (ادْعُوني) is an Arabic-first, RTL, anonymous (no-auth) Islamic du'a app.
This file is the **source of truth for how code in `apps/mobile` is organized**.
Follow it for every change. When a task conflicts with it, fix the structure to
match this file rather than working around it.

---

## 1. Core principle: Feature-First

Code is grouped by **feature** (a user-facing area of the app), not by technical
layer. Everything a feature needs lives under `lib/features/{feature}/`.
Anything shared by **two or more** features lives under `lib/core/`.

> Decision rule: *"Is this used by more than one feature?"*
> → **Yes** → it belongs in `core/`.
> → **No** → it belongs inside that one feature.

---

## 2. Feature folder structure (the law)

Every feature has **exactly these three folders**:

```
lib/features/{feature}/
├── repository/        # data access for this feature (talks to core/network + core/models)
├── controller/        # state + logic (Riverpod ChangeNotifier controllers + their providers)
└── screens/           # the screen(s) for this feature
    └── widgets/        # widgets used ONLY by this feature's screens
```

Rules:
- **`repository/`** — the feature's data source(s). Depends on `core/network`
  (the `ApiClient`) and returns `core/models`. **No Flutter/UI imports.** If a
  repository is needed by more than one feature, move it to `core/repositories/`.
- **`controller/`** — one `ChangeNotifier` per concern, each exposing its own
  Riverpod provider in the same file. Controllers depend on repositories, never on
  `ApiClient` directly. **No `BuildContext` in controllers.**
- **`screens/`** — the full-page widget(s) (`*_screen.dart`). Read state via
  `ref.watch` / `ref.read`. Keep thin: compose widgets, don't inline large trees.
- **`screens/widgets/`** — private, feature-only widgets. The moment a widget is
  reused by another feature, promote it to `core/widgets/` (§4).

A feature only creates the folders it actually uses. A feature reading a shared
repository from `core/` omits `repository/` — no empty folders, no pass-throughs.

---

## 3. The `core/` folder (shared across all features)

```
lib/core/
├── constants/         # app-wide constants (app_config.dart, strings, …)
├── network/           # ApiClient, ApiException — the single HTTP layer
├── error/             # Failure sealed types + exception→failure mapping (§7)
├── state/             # ViewState<T> async-state shape (§6)
├── models/            # plain data models (Prayer, …) + fromJson/toJson
├── repositories/      # data sources shared by >1 feature (Prayers, Taxonomy)
├── controllers/       # app-wide state with no single feature owner (Theme, Saved, Taxonomy)
├── services/          # platform/integration services (WidgetService)
├── theme/             # colors, typography, tokens, ThemeData — the design system (§8)
├── utils/             # small pure helpers (arabic_numbers, share_dua, …)
├── widgets/           # shared, reusable widgets (§4)
└── providers.dart     # Riverpod DI roots (sharedPreferences, repositories)
```

- `core/` must **not** import from `features/`. Dependencies point one way:
  `features/ → core/`, never the reverse.
- Models are dumb data: no business logic, no network calls.
- Shared controllers (e.g. `SavedController`) live in `core/controllers/`.

---

## 4. Reusable components (build once, share everywhere)

**Before building any UI piece, search `core/widgets/` for an existing component
and reuse it. Never re-implement or copy-paste a widget that already exists.**

- **Build for reuse from the start.** Data and callbacks go through the
  **constructor** (data in, events out). No hard-coded strings/colors/sizes — use
  design-system tokens (§8). Prefer `const` constructors.
- **Presentational only.** A widget does not fetch data, build repositories, or
  mutate app state. The one exception: reading genuinely-global shared state it is
  intrinsically about (e.g. `DuaCard` ↔ `SavedController`), via a provider.
- **Promote on second use** → move a feature widget to `core/widgets/` the moment
  a second feature needs it. Do not fork or copy.
- **Promote design-system primitives on first use** — pill/chip, card surface,
  select field, bottom sheet, labeled input, section header, empty state, button.
- **No near-duplicates** — extract one configurable widget, not two near-copies.
- **Every reusable widget**: light **and** dark, RTL-safe, documented params with
  sensible defaults, no feature-specific assumptions.

Existing shared components — **reuse / extend, don't re-create**: `DuaCard`,
`DuaHeroCard`, `BrandSelectField`, `BrandWordmark`, `MetaChips`, `SectionHeader`,
`EmptyState`, `NightBackground`. When touching a screen, audit it and lift any
reusable inline widget to `screens/widgets/` (feature-only) or `core/widgets/`
(shared).

---

## 5. State management: Riverpod

The app uses **`flutter_riverpod`** (the `provider` package is removed — never
re-introduce it).

- The app is wrapped in `ProviderScope` (`main.dart`); `sharedPreferencesProvider`
  is overridden there with the loaded instance.
- Each controller is a `ChangeNotifier` exposed via a `ChangeNotifierProvider`
  declared **in the same file**, right above the class:
  ```dart
  final homeControllerProvider =
      ChangeNotifierProvider.autoDispose<HomeController>(
    (ref) => HomeController(ref.watch(prayersRepositoryProvider)),
  );
  ```
- `.autoDispose` for screen-scoped controllers (Home, Add); non-disposed for
  app-wide ones (Theme, Saved, Taxonomy, Shell, Settings).
- Widgets reading providers are `ConsumerWidget` / `ConsumerStatefulWidget`;
  `ref.watch` to rebuild, `ref.read` for one-off actions (button taps).
- Inject deps through providers (`ref.watch(...)`), never construct inline.

---

## 6. Async state shape (one pattern everywhere)

Controllers do **not** expose loose public `bool loading` / `Object? error` /
`List results` fields. They expose a single immutable async state so every screen
reads it the same way.

Canonical type (in `core/state/view_state.dart`):

```dart
sealed class ViewState<T> {
  const ViewState();
}
class ViewLoading<T> extends ViewState<T> { const ViewLoading(); }
class ViewData<T>    extends ViewState<T> { final T value; const ViewData(this.value); }
class ViewError<T>   extends ViewState<T> { final Failure failure; const ViewError(this.failure); }
```

- A controller holds `ViewState<T> get state` (private setter) and emits new
  states via `notifyListeners()`.
- Screens `switch` over the state to render loading / data / error — no flag
  juggling:
  ```dart
  switch (controller.state) {
    ViewLoading() => const LoadingView(),
    ViewError(:final failure) => ErrorView(failure: failure, onRetry: controller.refresh),
    ViewData(:final value) => Content(value),
  }
  ```
- **Pagination/partial loads** (e.g. كل الأدعية) may extend with explicit extra
  flags (`loadingMore`, `hasMore`, `totalItems`) **on top of** the data state, but
  the base loading/error/data classification still flows through `ViewState`.
- Mutable user input that drives a query (search text, selected filters) stays as
  plain controller fields; only the **result** is a `ViewState`.

---

## 7. Errors & failures (typed, with Arabic messages)

No screen ever receives a raw `Object`/`Exception`. Errors are typed and carry a
user-facing message.

In `core/error/failure.dart`:

```dart
sealed class Failure {
  const Failure();
  String get messageAr;           // user-facing Arabic message
}
// e.g. NetworkFailure, TimeoutFailure, ServerFailure(int code),
//      NotFoundFailure, UnknownFailure
```

- **Repositories** (and `ApiClient`) translate exceptions/`ApiException` into a
  `Failure` — they never let a raw exception escape to a controller.
- **Controllers** store `Failure` (inside `ViewError`), never `Object? error`.
- **UI** renders `failure.messageAr` plus a **retry** affordance. Empty/silent
  error states are not acceptable — every failure shows a message and a way out.
- Keep messages short, Arabic, and human (e.g. "تعذّر الاتصال بالخادم. تحقّق من
  اتصالك."). Reuse `EmptyState` / a shared `ErrorView` to render them.

---

## 8. Design system & theme tokens (no magic values)

The brand design system in `core/theme/` is the **single source of truth** for
visual values. Widgets must not hard-code them.

- **Colors** → `AppColors` only. No `Color(0xFF…)` / `Colors.x` literals in
  feature or widget code.
- **Spacing / padding / gaps** → `AppSpacing`.
- **Radii** → `AppRadii`. **Typography** → `AppFonts`.
- If a needed value doesn't exist, **add it to the token file** and reference it —
  never inline a one-off.
- Brand gradients/shadows (e.g. the night gradient, the share-button gradient) are
  design-system elements: define them as named helpers/tokens in `core/theme`, not
  re-declared per widget.
- Allowed literals: `0`, and purely structural values (flex weights, `1` for a
  hairline divider, animation counts). Everything visual comes from tokens.

> This makes theming, dark-mode, and rebrands a one-file change, and is what makes
> the §4 reusable widgets truly portable.

---

## 9. Naming conventions

- Files: `snake_case.dart`, matching the primary type:
  `home_controller.dart` → `HomeController`.
- Repositories: `{feature}_repository.dart` → `{Feature}Repository`.
- Controllers: `{concern}_controller.dart` → `{Concern}Controller` +
  `{concern}ControllerProvider`.
- Screens: `{feature}_screen.dart` → `{Feature}Screen`.
- Feature-only widgets in `screens/widgets/`: `snake_case.dart`. Library-private
  (`_Foo`) only if used in one file; if shared across the feature, a public class
  in its own file.
- Arabic UI strings: centralize reused copy in `core/constants/strings.dart`; the
  app is Arabic-first and forces `Locale('ar')`. Keep RTL in mind.

---

## 10. Layering rules (enforced)

```
screens (UI)  →  controllers (state)  →  repositories (data)  →  network/models
```

- UI never calls `ApiClient` or builds a repository directly — go through a
  controller/provider.
- Controllers never import `package:flutter/material.dart` or use `BuildContext`.
- Repositories never import Flutter, never hold UI state, and map errors to
  `Failure` (§7).
- `core/` never imports `features/`.

---

## 11. Target structure (what the refactor produces)

```
lib/
├── main.dart
├── app.dart
├── core/
│   ├── constants/        app_config.dart, strings.dart
│   ├── network/          api_client.dart
│   ├── error/            failure.dart
│   ├── state/            view_state.dart
│   ├── models/           prayer.dart, prayer_category.dart, prayer_group.dart, prayer_type.dart
│   ├── repositories/     prayers_repository.dart, taxonomy_repository.dart
│   ├── controllers/      theme_controller.dart, saved_controller.dart, taxonomy_controller.dart
│   ├── services/         widget_service.dart
│   ├── theme/            app_colors.dart, app_theme.dart, app_tokens.dart, app_typography.dart
│   ├── utils/            arabic_numbers.dart, share_dua.dart
│   ├── widgets/          dua_card.dart, dua_hero_card.dart, brand_select.dart,
│   │                     brand_wordmark.dart, meta_chips.dart, empty_state.dart,
│   │                     error_view.dart, night_background.dart, section_header.dart
│   └── providers.dart
└── features/
    ├── home/
    │   ├── controller/   home_controller.dart
    │   └── screens/      home_screen.dart
    │       └── widgets/  greeting.dart, daily_section.dart, group_chips.dart
    ├── add_dua/
    │   ├── controller/   add_dua_controller.dart
    │   └── screens/      add_dua_screen.dart
    │       └── widgets/  type_segmented.dart, pending_note.dart, success_view.dart, field_label.dart
    ├── saved/
    │   ├── controller/   search_controller.dart
    │   └── screens/      saved_screen.dart
    │       └── widgets/  saved_tab.dart, search_tab.dart, filter_row.dart,
    │                     results_list.dart, load_more_footer.dart, offline_note.dart
    ├── settings/
    │   ├── controller/   settings_controller.dart
    │   └── screens/      settings_screen.dart
    │       └── widgets/  theme_card.dart, interval_card.dart, option_card.dart
    └── shell/
        ├── controller/   shell_controller.dart
        └── screens/      root_shell.dart
```

> `home`, `add_dua`, and `saved` read the **shared** `PrayersRepository` from
> `core/repositories/`, so they have no `repository/` folder of their own. A
> feature gets one only when it owns a data source no other feature uses.

---

## 12. Migration from the current structure

| Current | Target |
|---|---|
| `features/{f}/application/{f}_controller.dart` | `features/{f}/controller/{f}_controller.dart` |
| `features/{f}/presentation/{f}_screen.dart` | `features/{f}/screens/{f}_screen.dart` |
| inline `_Widget`s inside a screen | extracted into `screens/widgets/` (or `core/widgets/` if shared) |
| `core/data/prayers_repository.dart`, `taxonomy_repository.dart` | `core/repositories/` |
| `core/data/saved_controller.dart`, `taxonomy_controller.dart` | `core/controllers/` |
| raw `bool loading` / `Object? error` in controllers | `ViewState<T>` + `Failure` (§6, §7) |
| hard-coded colors/radii/sizes | `core/theme` tokens (§8) |
| `core/data/` (folder) | removed once emptied |

Rename `application/ → controller/`, `presentation/ → screens/`. Do it
feature-by-feature, keeping `flutter analyze` + tests green at every step.

---

## 13. Definition of done (every change)

- `flutter analyze` → **No issues found**.
- `flutter test` → all green (test controllers and repositories; deps come from
  providers/constructors, so they're injectable with fakes).
- Files placed per §2–§3; imports follow §10 layering (no upward deps).
- **Async state (§6):** controller exposes a `ViewState`, not loose flags.
- **Errors (§7):** failures are typed and rendered with an Arabic message + retry;
  no silent empty error states.
- **Theme tokens (§8):** no hard-coded colors/sizes/radii; missing values added to
  the token files.
- **Reusability (§4):** reused an existing `core/widgets/` component where one fit;
  new reusable/design-system widgets live in `core/widgets/`; no near-copies.
- No `package:provider`; no `BuildContext` in controllers/repositories.
- Arabic/RTL preserved.
