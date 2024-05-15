from ursina import *

# Initialize the 3D engine
app = Ursina()

# 1. Setting the Scene (Lighting and Camera)
window.title = "Hyper-Realistic Pong"
window.borderless = False
window.color = color.black

# Add a light to cast shadows
PointLight(parent=camera, position=(0, 10, -10))
AmbientLight(color=color.rgba(100, 100, 100, 0.1))

# Camera positioning (Isometric view)
camera.position = (0, 15, -20)
camera.rotation_x = 35

# 2. The Environment (The Table)
# We create a large cube for the floor/table
table = Entity(
    model='cube',
    color=color.rgb(30, 100, 50), # Felt Green
    scale=(20, 1, 10),
    position=(0, -1, 0),
    texture='white_cube',
    collider='box'
)

# The Net
net = Entity(
    model='cube',
    color=color.white,
    scale=(20, 0.5, 0.1),
    position=(0, 0.5, 0)
)

# 3. The Players (3D Paddles)
# Player 1 (Left)
player1 = Entity(
    model='cube',
    color=color.azure,
    scale=(1, 2, 4),
    position=(-8, 1, 0),
    collider='box',
    texture='white_cube' # Adds a bit of grain/realism
)

# Player 2 (Right - AI)
player2 = Entity(
    model='cube',
    color=color.orange,
    scale=(1, 2, 4),
    position=(8, 1, 0),
    collider='box',
    texture='white_cube'
)

# 4. The Ball (Physics based)
ball = Entity(
    model='sphere',
    color=color.white,
    scale=1,
    position=(0, 1, 0),
    collider='sphere',
    texture='noise' # Gives it a surface texture so we can see it spin
)

# Game Variables
ball.dx = 0.2
ball.dz = 0.15
player1_score = 0
player2_score = 0

# Score Text (UI)
score_text = Text(text='0 | 0', position=(0, 0.4), origin=(0, 0), scale=2, color=color.light_gray)

# 5. Game Logic
def update():
    global ball
    
    # Move Player 1 with Mouse Y (mapped to World Z)
    # We clamp the position so the paddle stays on the table
    player1.z += (mouse.y * 20 - player1.z) * 5 * time.dt
    player1.z = clamp(player1.z, -4, 4)

    # Simple AI for Player 2
    # It tries to match the ball's Z position
    player2.z += (ball.z - player2.z) * 4 * time.dt
    player2.z = clamp(player2.z, -4, 4)

    # Ball Movement
    ball.x += ball.dx
    ball.z += ball.dz
    
    # Spin effect (visual only)
    ball.rotation_y += 100 * time.dt

    # --- Collision Logic ---
    
    # Bounce off Top/Bottom walls (Table edges)
    if ball.z > 4.5 or ball.z < -4.5:
        ball.dz = -ball.dz
        # Add a little audio cue logic here if you had sound files

    # Paddle Collisions
    # Check if ball is touching Player 1
    if ball.x < -7 and ball.x > -8.5:
        if ball.z < player1.z + 2.5 and ball.z > player1.z - 2.5:
            ball.dx = -ball.dx
            ball.x = -7 # Prevent sticking
            # Increase speed slightly on hit
            ball.dx *= 1.05
            
    # Check if ball is touching Player 2
    if ball.x > 7 and ball.x < 8.5:
        if ball.z < player2.z + 2.5 and ball.z > player2.z - 2.5:
            ball.dx = -ball.dx
            ball.x = 7
            ball.dx *= 1.05

    # --- Scoring ---
    if ball.x < -10:
        reset_ball()
    elif ball.x > 10:
        reset_ball()

def reset_ball():
    global player1_score, player2_score
    ball.position = (0, 1, 0)
    
    # Reset speed but randomize direction
    ball.dx = 0.2 if random.random() > 0.5 else -0.2
    ball.dz = random.choice([-0.15, 0.15])

# Run the game
app.run()