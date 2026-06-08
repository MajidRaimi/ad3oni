import 'prayer_category.dart';
import 'prayer_type.dart';

/// A du'a from `/v1/prayers`. Carries its category & type expanded inline.
class Prayer {
  const Prayer({
    required this.id,
    required this.text,
    required this.status,
    this.source,
    this.category,
    this.type,
    this.created = '',
    this.updated = '',
  });

  final String id;
  final String text;
  final String status;

  /// Provenance of the du'a (e.g. "سنن أبي داود", "دعاء عام"), when known.
  final String? source;
  final PrayerCategory? category;
  final PrayerType? type;
  final String created;
  final String updated;

  String get categoryName => category?.name ?? '';
  String get typeName => type?.name ?? '';
  String get sourceName => source ?? '';

  factory Prayer.fromJson(Map<String, dynamic> json) => Prayer(
        id: (json['id'] ?? '').toString(),
        text: (json['text'] ?? '').toString(),
        status: (json['status'] ?? '').toString(),
        source: json['source'] is String && (json['source'] as String).isNotEmpty
            ? json['source'] as String
            : null,
        category: json['category'] is Map<String, dynamic>
            ? PrayerCategory.fromJson(json['category'] as Map<String, dynamic>)
            : null,
        type: json['type'] is Map<String, dynamic>
            ? PrayerType.fromJson(json['type'] as Map<String, dynamic>)
            : null,
        created: (json['created'] ?? '').toString(),
        updated: (json['updated'] ?? '').toString(),
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'text': text,
        'status': status,
        if (source != null) 'source': source,
        if (category != null) 'category': category!.toJson(),
        if (type != null) 'type': type!.toJson(),
        'created': created,
        'updated': updated,
      };

  @override
  bool operator ==(Object other) => other is Prayer && other.id == id;

  @override
  int get hashCode => id.hashCode;
}
