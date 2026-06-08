import 'dart:async';

import 'package:http/http.dart' as http;

import '../network/api_client.dart';

/// A typed, user-facing failure. Repositories translate exceptions into one of
/// these so controllers and UI never deal with raw `Object`/`Exception` — every
/// failure carries a short Arabic message and renders with a retry affordance.
sealed class Failure {
  const Failure();

  /// Short, human, Arabic message shown to the user.
  String get messageAr;
}

/// No / lost connection (DNS, socket, host unreachable).
class NetworkFailure extends Failure {
  const NetworkFailure();

  @override
  String get messageAr => 'تعذّر الاتصال. تحقّق من اتصالك بالإنترنت.';
}

/// The request took too long.
class TimeoutFailure extends Failure {
  const TimeoutFailure();

  @override
  String get messageAr => 'انتهت مهلة الاتصال. حاول مرة أخرى.';
}

/// The server responded with an error status (5xx, or unexpected 4xx).
class ServerFailure extends Failure {
  const ServerFailure(this.statusCode);
  final int statusCode;

  @override
  String get messageAr => 'تعذّر تحميل البيانات من الخادم. حاول لاحقًا.';
}

/// The requested resource does not exist (404).
class NotFoundFailure extends Failure {
  const NotFoundFailure();

  @override
  String get messageAr => 'لم يتم العثور على المحتوى المطلوب.';
}

/// Anything we didn't anticipate.
class UnknownFailure extends Failure {
  const UnknownFailure([this.cause]);
  final Object? cause;

  @override
  String get messageAr => 'حدث خطأ غير متوقّع. حاول مرة أخرى.';
}

/// Maps any thrown error to a typed [Failure]. Used in repository catch blocks
/// so a raw exception never escapes the data layer.
Failure failureFrom(Object error) {
  if (error is Failure) return error;
  if (error is TimeoutException) return const TimeoutFailure();
  // `http` throws ClientException for socket/connection problems on every
  // platform (avoids a `dart:io`-only SocketException, which breaks web).
  if (error is http.ClientException) return const NetworkFailure();
  if (error is ApiException) {
    if (error.statusCode == 404) return const NotFoundFailure();
    if (error.statusCode == 0) return const NetworkFailure();
    return ServerFailure(error.statusCode);
  }
  return UnknownFailure(error);
}
