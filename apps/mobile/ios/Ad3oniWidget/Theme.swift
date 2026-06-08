import SwiftUI
import WidgetKit

/// Ad3oni brand tokens, ported from the design system to SwiftUI.
enum Brand {
    static let royal = Color(hex: 0x2B0D69)
    static let violet = Color(hex: 0x6D49D6)
    static let lilac = Color(hex: 0xA98EE6)
    static let night = Color(hex: 0x0C0626)
    static let ink = Color(hex: 0x1A1330)

    // signature night radial gradient: #2c1370 -> #190b40 -> #0b0524
    static let nightTop = Color(hex: 0x2C1370)
    static let nightMid = Color(hex: 0x190B40)
    static let nightBottom = Color(hex: 0x0B0524)

    // "paper" (light) treatment
    static let paperTop = Color.white
    static let paperBottom = Color(hex: 0xF4F1FC)
    static let border = Color(hex: 0xE7E2F2)

    /// Brand display face (Rakkas), bundled with the extension.
    static func display(_ size: CGFloat) -> Font {
        Font.custom("Rakkas-Regular", size: size)
    }

    static func mono(_ size: CGFloat, weight: Font.Weight = .medium) -> Font {
        Font.system(size: size, weight: weight, design: .monospaced)
    }

    static func sans(_ size: CGFloat, weight: Font.Weight = .regular) -> Font {
        Font.system(size: size, weight: weight)
    }
}

/// Colours that flip between the night and paper treatments.
struct Palette {
    let isDark: Bool

    var dua: Color { isDark ? .white : Brand.ink }
    var wordmark: Color { isDark ? Color.white.opacity(0.85) : Brand.royal }
    var eyebrow: Color { isDark ? Brand.lilac : Brand.violet }
    var brace: Color { isDark ? Brand.lilac.opacity(0.5) : Brand.violet.opacity(0.4) }
    var date: Color { isDark ? Color(hex: 0xCDBCF2).opacity(0.7) : Brand.ink.opacity(0.5) }
    var tagText: Color { isDark ? Color.white.opacity(0.85) : Brand.royal }
    var tagBorder: Color { isDark ? Brand.lilac.opacity(0.32) : Brand.border }
    var tagFill: Color { isDark ? Brand.lilac.opacity(0.10) : Color(hex: 0xF4F1FC) }
    var divider: Color { isDark ? Brand.lilac.opacity(0.40) : Brand.violet.opacity(0.25) }
    var cached: Color { isDark ? Color.white.opacity(0.45) : Brand.ink.opacity(0.45) }
}

extension Color {
    init(hex: UInt32) {
        self.init(
            .sRGB,
            red: Double((hex >> 16) & 0xFF) / 255,
            green: Double((hex >> 8) & 0xFF) / 255,
            blue: Double(hex & 0xFF) / 255,
            opacity: 1
        )
    }
}

/// The brand background (night gradient + lilac glow, or paper) applied to the
/// home-screen widget families. Accessory (lock-screen) families stay clear so
/// the system can tint them.
struct WidgetBackground: View {
    let palette: Palette

    var body: some View {
        if palette.isDark {
            LinearGradient(
                colors: [Brand.nightTop, Brand.nightMid, Brand.nightBottom],
                startPoint: .top,
                endPoint: .bottom
            )
            .overlay(
                RadialGradient(
                    colors: [Brand.lilac.opacity(0.18), .clear],
                    center: UnitPoint(x: 0.5, y: 0.34),
                    startRadius: 2,
                    endRadius: 190
                )
            )
        } else {
            LinearGradient(
                colors: [Brand.paperTop, Brand.paperBottom],
                startPoint: .top,
                endPoint: .bottom
            )
            .overlay(
                RadialGradient(
                    colors: [Brand.violet.opacity(0.06), .clear],
                    center: UnitPoint(x: 0.5, y: 0.3),
                    startRadius: 2,
                    endRadius: 190
                )
            )
        }
    }
}

/// Applies the brand background, bridging the iOS 17 `containerBackground` API
/// and the older `.background` modifier.
struct BrandContainer: ViewModifier {
    let family: WidgetFamily
    let palette: Palette

    private var isAccessory: Bool {
        switch family {
        case .accessoryRectangular, .accessoryInline, .accessoryCircular:
            return true
        default:
            return false
        }
    }

    func body(content: Content) -> some View {
        if #available(iOS 17.0, *) {
            content.containerBackground(for: .widget) {
                if isAccessory {
                    Color.clear
                } else {
                    WidgetBackground(palette: palette)
                }
            }
        } else {
            if isAccessory {
                content
            } else {
                content.background(WidgetBackground(palette: palette))
            }
        }
    }
}

extension View {
    func brandContainer(family: WidgetFamily, palette: Palette) -> some View {
        modifier(BrandContainer(family: family, palette: palette))
    }
}
