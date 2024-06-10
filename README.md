# Projectile Motion Game #
My goal was to create an engaging game that focused on helping classmates practise projectile motion for the HSC. The objective of the game is to hit the target in one shot by deriving the equations of motion of the projectile (without air resistance).

## How I worked on this project ##
* I built this game using Python and Pygame.
* I derived and used the equations of motion with constant acceleration to position the target.
* I utilised online resources extensively:
  * https://youtu.be/_gDOz7E6HVM?si=MIr-12bOoBqkMYu_
  * https://youtu.be/Y4xlUNfrvow?si=w4F7xZbTMztjH4PN
  * https://youtu.be/xYhniILN6Ls?si=1K8Hfbo5_WmCnmwt

## Main Features ##
* __User Input__: Users can adjust the velocity and angle of projection of the ball to hit the target.
* __Projectile Motion Simulation__: The game simulates projectile motion by considering the user input.

## Why I built the project this way ##
* I avoided implementing collision mechanics as the goal of the game was to help students practise projectile motion. Collision mechanics are not typically used with projectile motion in the HSC.
* I created maps to simulate different planets by changing the theme and gravity of each level (Level 1 is Earth, Level 2 is the Moon, Level 3 is Uranus) as the HSC sometimes asks students to calculate the range of the projectile if it was projected on a different planet.

## If I had more time I would change this ##
* __Map Layout__: Right now, every level has the same map layout except for where the target is located. Instead I would of preferred if each level had a unique layout.
* __Collision Mechanics__: Although collision mechanics is not necessary to help students practice projectile motion, adding this feature would have improved the quality of the game.
* __Random Gravity__: Instead of simulating different planets, I could have randomised the gravity on each level increasing the amount of practice for the user.

## Game Controls ##
* __Mouse__: Adjusts the velocity and angle of projection of the ball.
* __Space__: Launches the projectile.
* __Up arrow key__: Next level.
* __Down arrow key__: Previous level.
