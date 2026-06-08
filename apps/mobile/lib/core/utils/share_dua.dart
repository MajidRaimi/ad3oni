import 'package:share_plus/share_plus.dart';

import '../models/prayer.dart';

/// Shares a du'a's text via the OS share sheet, signed with the wordmark.
Future<void> shareDua(Prayer prayer) async {
  await SharePlus.instance.share(
    ShareParams(text: '${prayer.text}\n\n— ادْعُوني'),
  );
}
