SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Asteroid settings
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 3.0  # Spawn a new asteroid every 3 seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

# Player settings
PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 180  # Degrees per second
PLAYER_SPEED = 300  # Pixels per second
PLAYER_LIVES = 30
PLAYER_RESPAWN_TIME = 2.0  # seconds

# Shot settings
SHOT_RADIUS = 3  # Smaller bullets
PLAYER_SHOOT_SPEED = 600  # Faster bullets
PLAYER_SHOOT_COOLDOWN = 0.15  # Add cooldown for better gameplay

# Scoring system
SCORE_LARGE_ASTEROID = 20
SCORE_MEDIUM_ASTEROID = 50
SCORE_SMALL_ASTEROID = 100

# Explosion settings
EXPLOSION_DURATION = 0.5  # seconds
EXPLOSION_PARTICLES = 8
