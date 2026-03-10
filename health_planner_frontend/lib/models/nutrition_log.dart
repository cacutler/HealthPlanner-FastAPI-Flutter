class NutritionModel {
  final String id;
  final String userId;
  final int calories;
  final double? proteinG;
  final double? carbsG;
  final double? fatG;
  final DateTime loggedAt;

  NutritionModel({
    required this.id,
    required this.userId,
    required this.calories,
    this.proteinG,
    this.carbsG,
    this.fatG,
    required this.loggedAt,
  });

  factory NutritionModel.fromJson(Map<String, dynamic> j) => NutritionModel(
    id: j['id'],
    userId: j['user_id'],
    calories: j['calories'],
    proteinG: j['protein_g'] != null
        ? (j['protein_g'] as num).toDouble()
        : null,
    carbsG: j['carbs_g'] != null ? (j['carbs_g'] as num).toDouble() : null,
    fatG: j['fat_g'] != null ? (j['fat_g'] as num).toDouble() : null,
    loggedAt: DateTime.parse(j['logged_at']),
  );
}
