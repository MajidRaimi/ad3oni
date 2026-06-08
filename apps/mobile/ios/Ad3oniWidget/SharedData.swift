import Foundation

/// Keys shared with the Flutter side (see lib/core/services/widget_service.dart).
enum SharedKeys {
    static let appGroup = "group.com.ad3oni.ad3oni"
    static let dailyText = "daily_text"
    static let dailyCategory = "daily_category"
    static let dailyType = "daily_type"
    static let pool = "pool_json"
    static let randomInterval = "random_interval_minutes"
}

/// A du'a as shown by the widgets.
struct Dua {
    let text: String
    let category: String
    let type: String

    var hasMeta: Bool { !category.isEmpty || !type.isEmpty }
}

extension Dua {
    /// Shown in the widget gallery / before the app has synced anything.
    static let sampleDaily = Dua(
        text: "اللّهمّ اغفر لي وارحمني واهدِني",
        category: "الاستغفار والتوبة",
        type: "نبوي"
    )

    static let samplePool = [
        Dua(text: "اللّهمّ إني أسألك العفوَ والعافية", category: "العافية", type: "نبوي"),
        Dua(text: "اللّهمّ اجعل القرآنَ ربيعَ قلبي", category: "القرآن", type: "نبوي"),
        Dua(text: "ربِّ اشرح لي صدري ويسّر لي أمري", category: "الكرب والشدة", type: "قرآني"),
        Dua(text: "ربَّنا آتِنا في الدنيا حسنةً", category: "الجامعة", type: "قرآني"),
    ]
}

/// Reads the App Group store that the Flutter app writes to.
enum DataStore {
    private static var defaults: UserDefaults? {
        UserDefaults(suiteName: SharedKeys.appGroup)
    }

    static func dailyDua() -> Dua? {
        guard let d = defaults,
              let text = d.string(forKey: SharedKeys.dailyText),
              !text.isEmpty
        else { return nil }
        return Dua(
            text: text,
            category: d.string(forKey: SharedKeys.dailyCategory) ?? "",
            type: d.string(forKey: SharedKeys.dailyType) ?? ""
        )
    }

    /// How often the random widget rotates, in minutes. Falls back to 120
    /// (every 2 hours) when the app hasn't written a value yet.
    static func randomIntervalMinutes() -> Int {
        guard let d = defaults else { return 120 }
        let raw = d.integer(forKey: SharedKeys.randomInterval)
        return raw > 0 ? raw : 120
    }

    static func pool() -> [Dua] {
        guard let d = defaults,
              let json = d.string(forKey: SharedKeys.pool),
              let data = json.data(using: .utf8),
              let array = try? JSONSerialization.jsonObject(with: data) as? [[String: Any]]
        else { return [] }

        return array.compactMap { item in
            guard let text = item["text"] as? String, !text.isEmpty else { return nil }
            return Dua(
                text: text,
                category: item["category"] as? String ?? "",
                type: item["type"] as? String ?? ""
            )
        }
    }
}

/// Today's Hijri date, formatted in Arabic (e.g. "٢٢ ذو القعدة ١٤٤٧ هـ").
/// Computed natively so it stays correct as days pass without an app launch.
enum HijriDate {
    static func today() -> String {
        var calendar = Calendar(identifier: .islamicUmmAlQura)
        calendar.locale = Locale(identifier: "ar")
        let formatter = DateFormatter()
        formatter.calendar = calendar
        formatter.locale = Locale(identifier: "ar")
        formatter.dateFormat = "d MMMM yyyy"
        return formatter.string(from: Date()) + " هـ"
    }
}
