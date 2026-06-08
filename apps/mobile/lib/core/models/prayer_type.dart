/// A source type (قرآني · نبوي · أثري · مخصص). `/v1/types`.
class PrayerType {
  const PrayerType({required this.id, required this.name, required this.slug});

  final String id;
  final String name;
  final String slug;

  factory PrayerType.fromJson(Map<String, dynamic> json) => PrayerType(
        id: (json['id'] ?? '').toString(),
        name: (json['name'] ?? '').toString(),
        slug: (json['slug'] ?? '').toString(),
      );

  Map<String, dynamic> toJson() => {'id': id, 'name': name, 'slug': slug};
}
