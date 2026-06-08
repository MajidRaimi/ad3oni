import '../error/failure.dart';

/// One immutable shape for asynchronously-loaded data, so every screen reads
/// loading / data / error the same way (see CLAUDE.md §6).
///
/// Screens `switch` over it instead of juggling `loading`/`error`/`data` flags:
/// ```dart
/// switch (controller.state) {
///   ViewLoading() => const LoadingView(),
///   ViewError(:final failure) => ErrorView(failure: failure, onRetry: ...),
///   ViewData(:final value) => Content(value),
/// }
/// ```
sealed class ViewState<T> {
  const ViewState();

  /// The data if this is a [ViewData], otherwise null.
  T? get dataOrNull => switch (this) {
        ViewData(:final value) => value,
        _ => null,
      };

  bool get isLoading => this is ViewLoading<T>;
}

/// The first load is in flight and there is nothing to show yet.
class ViewLoading<T> extends ViewState<T> {
  const ViewLoading();
}

/// Data is available.
class ViewData<T> extends ViewState<T> {
  const ViewData(this.value);
  final T value;
}

/// The load failed; carries a typed [Failure] with a user-facing message.
class ViewError<T> extends ViewState<T> {
  const ViewError(this.failure);
  final Failure failure;
}
