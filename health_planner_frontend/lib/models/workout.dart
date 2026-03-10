class WeightLogModel {
  final String id;
  final String userId;
  final double weightLbs;
  final DateTime loggedAt;

  WeightLogModel({
    required this.id,
    required this.userId,
    required this.weightLbs,
    required this.loggedAt,
  });

  factory WeightLogModel.fromJson(Map<String, dynamic> j) => WeightLogModel(
    id: j['id'],
    userId: j['user_id'],
    weightLbs: (j['weight_lbs'] as num).toDouble(),
    loggedAt: DateTime.parse(j['logged_at']),
  );
}
