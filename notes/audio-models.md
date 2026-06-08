# Audio Generation Models on Replicate

Best models for ambient/drone/bell-tone music:

1. stability-ai/stable-audio-2.5 - Long-form (up to ~3min), high quality, open-source
   - Supports inpainting and continuation
   - Example: replicate run stability-ai/stable-audio-2.5 --input prompt="..."

2. meta/musicgen - Simple, well-documented, 3.4M+ runs
   - Versions: stereo-melody-large (default), stereo-large, melody-large, large
   - Cookbook example: replicate run meta/musicgen --input prompt="slow ambient drone with bell harmonics" --input duration=20

3. lucataco/magnet - Fast non-autoregressive generation
   - Good for rapid iteration

4. google/lyria-2 - 48kHz stereo, highest fidelity, negative prompts supported
   - 30-second clips

5. lucataco/ace-step - Newer foundation model, recommended in Replicate collection

6. zsxkib/flux-music - Rectified Flow Transformer, outputs WAV + spectrogram

For ambient/drone: stable-audio-2.5 > meta/musicgen > magnet
