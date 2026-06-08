import 'prayer_group.dart';

/// A topic belonging to a [PrayerGroup]. `/v1/categories`.
class PrayerCategory {
  const PrayerCategory({
    required this.id,
    required this.name,
    required this.slug,
    this.group,
  });

  final String id;
  final String name;
  final String slug;
  final PrayerGroup? group;

  String? get groupSlug => group?.slug;
  String? get groupId => group?.id;

  factory PrayerCategory.fromJson(Map<String, dynamic> json) => PrayerCategory(
        id: (json['id'] ?? '').toString(),
        name: (json['name'] ?? '').toString(),
        slug: (json['slug'] ?? '').toString(),
        group: json['group'] is Map<String, dynamic>
            ? PrayerGroup.fromJson(json['group'] as Map<String, dynamic>)
            : null,
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        'slug': slug,
        if (group != null) 'group': group!.toJson(),
      };
}
