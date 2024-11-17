# Torbin2's Platformer TAS Competition Regulations
Version: 3 November 2024

### Wording
Uses of the words "must", "must not", "should", "should not" and "may" match [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## Article 1: Movie Format

- 1a) The submitted file must:  
    - 1a1) be a Platformer TAS Movie file, which at least fully works with commit [8ee94bcc0048a5833f502d2d5c5abc3acc17b989](https://github.com/Torbin2/platformer/commit/8ee94bcc0048a5833f502d2d5c5abc3acc17b989);
    - 1a2) not include any data which leads to an arbitery code execution;
    - 1a3) not include "savestate" data;
    - 1a4) not have data size greater than 25 kiB;
    - 1a5) have "gameversion" data with constant value of "191";
    - 1a6) have "author" data with the authors of the TAS Movie.

- 1b) The submitted file should have extension name ".ptm".

## Article 2: Movie Replay

- 2a) The movie during the replay must:
  - 2a1) not include any input data which leads to an arbitery code execution;
  - 2a2) not include any input data that has more than 5 inputs in the same frame;
  - 2a3) not include any input data which presses keys except:
    - 2a3a) "pygame.K_a", "pygame.K_d", "pygame.K_SPACE", "pygame.K_r", "pygame.K_t";  
  - 2a4) work at 60 fps;
  - 2a6) at least have a movie length of 61 frames.
  
- 2b) The movie file with least amount of frames that leads to beating the game at final level wins the competition.
  - 2b1) The empty frames counts as a frame.

## Article 3: Replay and Competition Environment

- 3a) The replay environment must match the following:
  - 3a1) Python 3.12.*; 
  - 3a2) Pygame 2.6.*;
  - 3a3) main.py 1.9.1.
  
- 3b) The movie should be played back in 60 fps with frame advance off.