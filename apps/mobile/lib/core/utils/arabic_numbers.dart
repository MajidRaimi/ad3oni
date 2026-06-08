/// Converts Western digits in a string to Arabic-Indic digits (٠١٢٣…).
String toArabicDigits(String input) {
  const western = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
  const arabic = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
  var out = input;
  for (var i = 0; i < western.length; i++) {
    out = out.replaceAll(western[i], arabic[i]);
  }
  return out;
}
