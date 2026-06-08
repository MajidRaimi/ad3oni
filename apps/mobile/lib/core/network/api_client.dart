import 'dart:convert';

import 'package:http/http.dart' as http;

import '../constants/app_config.dart';

/// Thrown when the API returns a non-2xx response.
class ApiException implements Exception {
  ApiException(this.statusCode, [this.message]);
  final int statusCode;
  final String? message;

  @override
  String toString() => 'ApiException($statusCode): ${message ?? ''}';
}

/// Thin JSON client over the Ad3oni API. Anonymous (no auth headers).
class ApiClient {
  ApiClient({http.Client? client, String? baseUrl})
      : _client = client ?? http.Client(),
        _baseUrl = baseUrl ?? AppConfig.apiBaseUrl;

  /// Shared instance for the app.
  static final ApiClient instance = ApiClient();

  final http.Client _client;
  final String _baseUrl;

  static const _timeout = Duration(seconds: 20);

  Uri _uri(String path, [Map<String, String?>? query]) {
    final cleaned = <String, String>{};
    query?.forEach((k, v) {
      if (v != null && v.isNotEmpty) cleaned[k] = v;
    });
    return Uri.parse('$_baseUrl$path').replace(
      queryParameters: cleaned.isEmpty ? null : cleaned,
    );
  }

  /// GET returning a decoded JSON object.
  Future<Map<String, dynamic>> getJson(String path, {Map<String, String?>? query}) async {
    final res = await _client.get(_uri(path, query)).timeout(_timeout);
    return _decode(res) as Map<String, dynamic>;
  }

  /// GET returning a decoded JSON array.
  Future<List<dynamic>> getList(String path, {Map<String, String?>? query}) async {
    final res = await _client.get(_uri(path, query)).timeout(_timeout);
    return _decode(res) as List<dynamic>;
  }

  /// POST a JSON body, returning the decoded JSON object.
  Future<Map<String, dynamic>> postJson(String path, Map<String, dynamic> body) async {
    final res = await _client
        .post(
          _uri(path),
          headers: const {'Content-Type': 'application/json'},
          body: jsonEncode(body),
        )
        .timeout(_timeout);
    return _decode(res) as Map<String, dynamic>;
  }

  dynamic _decode(http.Response res) {
    if (res.statusCode >= 200 && res.statusCode < 300) {
      if (res.bodyBytes.isEmpty) return const <String, dynamic>{};
      return jsonDecode(utf8.decode(res.bodyBytes));
    }
    String? message;
    try {
      final body = jsonDecode(utf8.decode(res.bodyBytes));
      if (body is Map && body['detail'] != null) message = body['detail'].toString();
    } catch (_) {
      // non-JSON error body
    }
    throw ApiException(res.statusCode, message);
  }
}
