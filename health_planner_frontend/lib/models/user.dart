class UserModel {
  final String id;
  final String email;
  final int? heightIn;
  final int? weightLbs;
  final int? age;
  final String? sex;
  final String? activityLevel;
  final DateTime createdAt;

  UserModel({
    required this.id,
    required this.email,
    this.heightIn,
    this.weightLbs,
    this.age,
    this.sex,
    this.activityLevel,
    required this.createdAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> j) => UserModel(
    id: j['id'],
    email: j['email'],
    heightIn: j['height_in'],
    weightLbs: j['weight_lbs'],
    age: j['age'],
    sex: j['sex'],
    activityLevel: j['activity_level'],
    createdAt: DateTime.parse(j['created_at']),
  );
}
