import SwiftUI
import WidgetKit

/// Routes a timeline entry to the right layout for the widget family, applies
/// the brand background, and forces RTL.
struct DuaWidgetView: View {
    @Environment(\.widgetFamily) private var family
    @Environment(\.colorScheme) private var colorScheme
    let entry: DuaEntry

    var body: some View {
        let palette = Palette(isDark: colorScheme == .dark)

        Group {
            switch family {
            case .systemSmall:
                SmallDuaView(entry: entry, palette: palette)
            case .systemMedium:
                MediumDuaView(entry: entry, palette: palette)
            case .systemLarge:
                LargeDuaView(entry: entry, palette: palette)
            case .accessoryRectangular:
                RectangularDuaView(entry: entry)
            case .accessoryInline:
                Label("﴿ \(entry.dua.text) ﴾", systemImage: entry.isRandom ? "shuffle" : "sparkles")
            default:
                SmallDuaView(entry: entry, palette: palette)
            }
        }
        .environment(\.layoutDirection, .rightToLeft)
        .brandContainer(family: family, palette: palette)
    }
}

// MARK: - Shared pieces

private struct Eyebrow: View {
    let entry: DuaEntry
    let palette: Palette

    var body: some View {
        HStack(spacing: 6) {
            Image(systemName: entry.isRandom ? "shuffle" : "sparkles")
                .font(.system(size: 9, weight: .semibold))
            Text(entry.isRandom ? "عشوائي" : "دعاء اليوم")
                .font(Brand.mono(9, weight: .semibold))
                .tracking(2)
        }
        .foregroundColor(palette.eyebrow)
    }
}

private struct Wordmark: View {
    let palette: Palette
    var size: CGFloat = 18
    var body: some View {
        Text("ادْعُوني")
            .font(Brand.display(size))
            .foregroundColor(palette.wordmark)
    }
}

private struct Tag: View {
    let label: String
    let palette: Palette
    var body: some View {
        Text(label)
            .font(Brand.sans(10, weight: .medium))
            .foregroundColor(palette.tagText)
            .lineLimit(1)
            .padding(.horizontal, 9)
            .padding(.vertical, 3)
            .background(
                Capsule().fill(palette.tagFill)
                    .overlay(Capsule().stroke(palette.tagBorder, lineWidth: 1))
            )
    }
}

private struct CachedNote: View {
    let palette: Palette
    var body: some View {
        HStack(spacing: 5) {
            Image(systemName: "wifi.slash").font(.system(size: 9))
            Text("من محفوظاتك").font(Brand.mono(9))
        }
        .foregroundColor(palette.cached)
    }
}

/// The du'a text flanked by brand braces.
private struct Quote: View {
    let text: String
    let palette: Palette
    var duaSize: CGFloat
    var braceSize: CGFloat
    var lineLimit: Int

    var body: some View {
        HStack(alignment: .center, spacing: 8) {
            Text("{")
                .font(Brand.display(braceSize))
                .foregroundColor(palette.brace)
            Text(text)
                .font(Brand.display(duaSize))
                .foregroundColor(palette.dua)
                .multilineTextAlignment(.center)
                .lineSpacing(5)
                .lineLimit(lineLimit)
                .minimumScaleFactor(0.6)
            Text("}")
                .font(Brand.display(braceSize))
                .foregroundColor(palette.brace)
        }
        // The braces are decorative and must always read "{ … }" (open on the
        // left, close on the right). Pin this row to LTR so the surrounding
        // RTL layout doesn't reverse the brace order; the Arabic du'a text is
        // strong-RTL and still renders correctly inside.
        .environment(\.layoutDirection, .leftToRight)
        .shadow(color: palette.isDark ? Brand.lilac.opacity(0.30) : .clear, radius: 18)
    }
}

// MARK: - Small (2×2)

private struct SmallDuaView: View {
    let entry: DuaEntry
    let palette: Palette

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            Eyebrow(entry: entry, palette: palette)
            Spacer(minLength: 8)
            Text(entry.dua.text)
                .font(Brand.display(16))
                .foregroundColor(palette.dua)
                .multilineTextAlignment(.center)
                .lineSpacing(4)
                .lineLimit(4)
                .minimumScaleFactor(0.6)
                .frame(maxWidth: .infinity, alignment: .center)
            Spacer(minLength: 8)
            HStack {
                Wordmark(palette: palette, size: 17)
                Spacer()
                if entry.isRandom {
                    Image(systemName: "wifi.slash")
                        .font(.system(size: 10))
                        .foregroundColor(palette.cached)
                }
            }
        }
        .padding(16)
    }
}

// MARK: - Medium (4×2)

private struct MediumDuaView: View {
    let entry: DuaEntry
    let palette: Palette

    var body: some View {
        HStack(spacing: 14) {
            Quote(text: entry.dua.text, palette: palette, duaSize: 19, braceSize: 30, lineLimit: 3)
                .frame(maxWidth: .infinity)

            VStack(alignment: .trailing, spacing: 8) {
                Wordmark(palette: palette, size: 18)
                Spacer()
                if entry.dua.type.isEmpty == false {
                    Tag(label: entry.dua.type, palette: palette)
                }
                if entry.isRandom {
                    CachedNote(palette: palette)
                } else {
                    Eyebrow(entry: entry, palette: palette)
                }
            }
        }
        .padding(.horizontal, 18)
        .padding(.vertical, 16)
    }
}

// MARK: - Large (4×4)

private struct LargeDuaView: View {
    let entry: DuaEntry
    let palette: Palette

    var body: some View {
        VStack(spacing: 0) {
            HStack {
                Wordmark(palette: palette, size: 22)
                Spacer()
                Eyebrow(entry: entry, palette: palette)
            }

            Spacer(minLength: 10)

            VStack(spacing: 12) {
                Quote(text: entry.dua.text, palette: palette, duaSize: 23, braceSize: 44, lineLimit: 5)
                Text(HijriDate.today())
                    .font(Brand.mono(11))
                    .foregroundColor(palette.date)
                HStack(spacing: 7) {
                    if entry.dua.category.isEmpty == false {
                        Tag(label: entry.dua.category, palette: palette)
                    }
                    if entry.dua.type.isEmpty == false {
                        Tag(label: entry.dua.type, palette: palette)
                    }
                }
            }

            Spacer(minLength: 10)

            HStack(spacing: 9) {
                HStack(spacing: 8) {
                    Image(systemName: "square.and.arrow.up").font(.system(size: 14, weight: .semibold))
                    Text("شارك").font(Brand.sans(15, weight: .bold))
                }
                .foregroundColor(Brand.night)
                .frame(maxWidth: .infinity)
                .frame(height: 42)
                .background(
                    Capsule().fill(
                        LinearGradient(colors: [Color(hex: 0xB9A2EC), Brand.lilac],
                                       startPoint: .top, endPoint: .bottom)
                    )
                )

                Image(systemName: entry.isRandom ? "wifi.slash" : "bookmark")
                    .font(.system(size: 16))
                    .foregroundColor(palette.isDark ? .white : Brand.royal)
                    .frame(width: 46, height: 42)
                    .background(
                        Capsule()
                            .fill(palette.isDark ? Color.white.opacity(0.05) : Color.white.opacity(0.6))
                            .overlay(Capsule().stroke(
                                palette.isDark ? Color.white.opacity(0.22) : Brand.border, lineWidth: 1))
                    )
            }
        }
        .padding(22)
    }
}

// MARK: - Lock screen (accessoryRectangular)

private struct RectangularDuaView: View {
    let entry: DuaEntry

    var body: some View {
        HStack(spacing: 8) {
            Image(systemName: entry.isRandom ? "shuffle" : "sparkles")
                .font(.system(size: 13, weight: .semibold))
            VStack(alignment: .leading, spacing: 1) {
                Text(entry.isRandom ? "عشوائي" : "دعاء اليوم")
                    .font(Brand.mono(9, weight: .semibold))
                    .widgetAccentable()
                Text(entry.dua.text)
                    .font(.system(size: 13, weight: .medium))
                    .lineLimit(2)
                    .minimumScaleFactor(0.7)
            }
            Spacer(minLength: 0)
        }
    }
}
