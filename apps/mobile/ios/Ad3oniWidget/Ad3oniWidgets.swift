import SwiftUI
import WidgetKit

/// A single rendered du'a at a point in the timeline.
struct DuaEntry: TimelineEntry {
    let date: Date
    let dua: Dua
    let isRandom: Bool
}

// MARK: - دعاء اليوم (today's du'a)

struct DailyProvider: TimelineProvider {
    func placeholder(in context: Context) -> DuaEntry {
        DuaEntry(date: Date(), dua: .sampleDaily, isRandom: false)
    }

    func getSnapshot(in context: Context, completion: @escaping (DuaEntry) -> Void) {
        completion(DuaEntry(date: Date(), dua: DataStore.dailyDua() ?? .sampleDaily, isRandom: false))
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<DuaEntry>) -> Void) {
        let dua = DataStore.dailyDua() ?? .sampleDaily
        let entry = DuaEntry(date: Date(), dua: dua, isRandom: false)

        // Refresh just after the next midnight so the Hijri date / daily du'a roll over.
        let midnight = Calendar.current.nextDate(
            after: Date(),
            matching: DateComponents(hour: 0, minute: 1),
            matchingPolicy: .nextTime
        ) ?? Date().addingTimeInterval(3600)

        completion(Timeline(entries: [entry], policy: .after(midnight)))
    }
}

struct Ad3oniDailyWidget: Widget {
    let kind = "Ad3oniDailyWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: DailyProvider()) { entry in
            DuaWidgetView(entry: entry)
        }
        .configurationDisplayName("دعاء اليوم")
        .description("دعاء اليوم من ادْعُوني، يتجدّد كل يوم.")
        .supportedFamilies([
            .systemSmall, .systemMedium, .systemLarge,
            .accessoryRectangular, .accessoryInline,
        ])
    }
}

// MARK: - عشوائي (random from the cached/saved pool)

struct RandomProvider: TimelineProvider {
    func placeholder(in context: Context) -> DuaEntry {
        DuaEntry(date: Date(), dua: Dua.samplePool[0], isRandom: true)
    }

    func getSnapshot(in context: Context, completion: @escaping (DuaEntry) -> Void) {
        let pool = DataStore.pool()
        let dua = pool.first ?? Dua.samplePool[0]
        completion(DuaEntry(date: Date(), dua: dua, isRandom: true))
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<DuaEntry>) -> Void) {
        var pool = DataStore.pool()
        if pool.isEmpty { pool = Dua.samplePool }

        // Rotation cadence the user picked in the app's settings (minutes).
        let interval = max(DataStore.randomIntervalMinutes(), 5)

        // Pre-render enough entries to span ~24h (capped), spaced `interval`
        // minutes apart. Re-shuffling each pass keeps small pools from settling
        // into a fixed A/B order. iOS shows these without a reload per step;
        // `.atEnd` then asks for a fresh (re-shuffled) timeline.
        let horizonMinutes = 24 * 60
        let maxEntries = 50
        let needed = max(2, min(horizonMinutes / interval, maxEntries))

        var sequence: [Dua] = []
        while sequence.count < needed {
            sequence.append(contentsOf: pool.shuffled())
        }

        var entries: [DuaEntry] = []
        let now = Date()
        for i in 0..<needed {
            let date = Calendar.current.date(byAdding: .minute, value: i * interval, to: now) ?? now
            entries.append(DuaEntry(date: date, dua: sequence[i], isRandom: true))
        }

        completion(Timeline(entries: entries, policy: .atEnd))
    }
}

struct Ad3oniRandomWidget: Widget {
    let kind = "Ad3oniRandomWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: RandomProvider()) { entry in
            DuaWidgetView(entry: entry)
        }
        .configurationDisplayName("دعاء عشوائي")
        .description("دعاء عشوائي من أدعيتك المحفوظة — يعمل دون اتصال.")
        .supportedFamilies([
            .systemSmall, .systemMedium, .systemLarge,
            .accessoryRectangular,
        ])
    }
}

// MARK: - Bundle

@main
struct Ad3oniWidgetBundle: WidgetBundle {
    var body: some Widget {
        Ad3oniDailyWidget()
        Ad3oniRandomWidget()
    }
}
