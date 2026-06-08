/// A top-level theme (e.g. مواقف الحياة). `/v1/groups`.
class PrayerGroup {
  const PrayerGroup({required this.id, required this.name, required this.slug});

  final String id;
  final String name;
  final String slug;

  factory PrayerGroup.fromJson(Map<String, dynamic> json) => PrayerGroup(
        id: (json['id'] ?? '').toString(),
        name: (json['name'] ?? '').toString(),
        slug: (json['slug'] ?? '').toString(),
      );

  Map<String, dynamic> toJson() => {'id': id, 'name': name, 'slug': slug};
}
