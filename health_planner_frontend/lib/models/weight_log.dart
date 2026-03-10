class ExerciseModel {
  final String id;
  final String workoutId;
  final String name;
  final int? sets;
  final int? reps;
  final double? weightLbs;
  final int? durationSeconds;

  ExerciseModel({
    required this.id,
    required this.workoutId,
    required this.name,
    this.sets,
    this.reps,
    this.weightLbs,
    this.durationSeconds,
  });

  factory ExerciseModel.fromJson(Map<String, dynamic> j) => ExerciseModel(
    id: j['id'],
    workoutId: j['workout_id'],
    name: j['name'],
    sets: j['sets'],
    reps: j['reps'],
    weightLbs: j['weight_lbs'] != null
        ? (j['weight_lbs'] as num).toDouble()
        : null,
    durationSeconds: j['duration_seconds'],
  );
}

class WorkoutModel {
  final String id;
  final String userId;
  final String type; // "strength" | "cardio"
  final int durationMinutes;
  final String intensity; // "low" | "medium" | "high"
  final int? caloriesBurned;
  final DateTime performedAt;
  final DateTime createdAt;
  final List<ExerciseModel> exercises;

  WorkoutModel({
    required this.id,
    required this.userId,
    required this.type,
    required this.durationMinutes,
    required this.intensity,
    this.caloriesBurned,
    required this.performedAt,
    required this.createdAt,
    required this.exercises,
  });

  factory WorkoutModel.fromJson(Map<String, dynamic> j) => WorkoutModel(
    id: j['id'],
    userId: j['user_id'],
    type: j['type'],
    durationMinutes: j['duration_minutes'],
    intensity: j['intensity'],
    caloriesBurned: j['calories_burned'],
    performedAt: DateTime.parse(j['performed_at']),
    createdAt: DateTime.parse(j['created_at']),
    exercises: (j['exercises'] as List<dynamic>? ?? [])
        .map((e) => ExerciseModel.fromJson(e))
        .toList(),
  );
}
