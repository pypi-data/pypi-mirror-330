import typing as tp
import torch
import torchaudio
import torch.nn.functional as F
import torchaudio.functional as taF

# def apply_reverb(*, 
#          audio_path: tp.Union[str, None] = None, 
#          audio_wav: tp.Union[torch.Tensor, None] = None, 
#          audio_wav_sr: tp.Union[int, None] = None,
#          ir_path: tp.Union[str, None] = None,
#          ir_wav: tp.Union[torch.Tensor, None] = None, 
#          ir_wav_sr: tp.Union[int, None] = None,
#          output_path: tp.Union[str, None] = None,
#          ) -> tp.Tuple[torch.Tensor, torch.Tensor, int]:
#     """
#     Apply convolution reverb to an audio file or tensor using torch.nn.functional.conv1d.

#     The audio input can be provided as either:
#       - A tensor of shape (n_channels, n_samples) (single example), or
#       - A tensor of shape (batch_size, n_channels, n_samples).
      
#     In the single-example case the tensor is automatically unsqueezed to add a batch dimension.

#     Args:
#         audio_path: Path to the input audio file.
#         audio_wav: Input audio as a torch.Tensor (n_channels, n_samples) or (batch_size, n_channels, n_samples).
#         audio_wav_sr: Sampling rate of the input audio.
#         ir_path: Path to the impulse response file.
#         ir_wav: Impulse response as a torch.Tensor (n_channels, n_samples).
#         ir_wav_sr: Sampling rate of the impulse response.
#         output_path: Path where the output audio will be saved.
#         use_partitioned: If True, processes the audio in blocks (overlap‑add) to reduce memory usage.
#         block_size: Block size (in samples) to use for partitioned convolution. If not provided and 
#                     use_partitioned is True, defaults to 10 seconds of audio (sr_audio * 10).
                    
#     Returns:
#         Tuple containing:
#         - Original mono audio waveform (torch.Tensor) with shape (batch_size, 1, n_samples)
#         - Convolved audio waveform (torch.Tensor) with shape (batch_size, 1, n_samples)
#         - Sample rate (int)
#     """
#     # Validate audio input
#     if audio_path is None and audio_wav is None:
#         raise ValueError("Either audio_path or audio_wav must be provided.")
#     if isinstance(audio_path, str) and audio_wav is not None:
#         raise ValueError("Only one of audio_path or audio_wav can be provided.")

#     # Load audio
#     if audio_path is not None:
#         audio_waveform, sr_audio = torchaudio.load(audio_path)  # shape: (n_channels, n_samples)
#         # Add a batch dimension: (1, n_channels, n_samples)
#         audio_waveform = audio_waveform.unsqueeze(0)
#     else:
#         audio_waveform = audio_wav
#         sr_audio = audio_wav_sr
#         # If provided as (n_channels, n_samples), unsqueeze to get (1, n_channels, n_samples)
#         if audio_waveform.dim() == 2:
#             audio_waveform = audio_waveform.unsqueeze(0)
#         elif audio_waveform.dim() != 3:
#             raise ValueError("audio_wav must be a 2D or 3D tensor.")

#     # Load impulse response (IR)
#     if ir_path is not None:
#         ir_waveform, sr_ir = torchaudio.load(ir_path)  # shape: (n_channels, n_samples)
#     else:
#         if ir_wav is None:
#             raise ValueError("Either ir_path or ir_wav must be provided.")
#         ir_waveform, sr_ir = ir_wav, ir_wav_sr
#         if ir_waveform.dim() != 2:
#             raise ValueError("ir_wav must be a 2D tensor of shape (n_channels, n_samples).")

#     # Ensure the sampling rates match; resample IR if needed.
#     if sr_audio != sr_ir:
#         ir_waveform = torchaudio.functional.resample(ir_waveform, sr_ir, sr_audio)

#     # Convert multi-channel audio to mono by averaging channels.
#     # For audio_waveform: shape (batch_size, n_channels, n_samples)
#     if audio_waveform.shape[1] > 1:
#         audio_waveform = audio_waveform.mean(dim=1, keepdim=True)
#     # For ir_waveform: shape (n_channels, n_samples)
#     if ir_waveform.shape[0] > 1:
#         ir_waveform = ir_waveform.mean(dim=0, keepdim=True)
    
#     # Remove the channel dimension for further processing and ensure float32.
#     # audio_batch: shape (batch_size, n_samples)
#     audio_batch = audio_waveform.squeeze(1).float()
#     batch_size, audio_length = audio_batch.shape

#     # Prepare the impulse response.
#     # Use the IR as a 1D tensor and flip it to convert PyTorch's cross-correlation into a true convolution.
#     ir = ir_waveform.squeeze(0).float()  # shape: (ir_length,)
#     ir = ir.flip(-1)
#     ir_length = ir.numel()
#     # Prepare IR kernel for conv1d: shape (1, 1, ir_length)
#     ir_kernel = ir.view(1, 1, ir_length)

#     # noramlize ir
#     # to distribute the energy, making its gain a unit gain.
#     # by doing this, the convolution doesn’t attenuate (or amplify) the overall energy of the speech signal.
#     ir_kernel = ir_kernel / ir_kernel.norm(p=2)  

#     # Process the entire audio at once.
#     # Pad the audio on the right so that conv1d produces an output of the same length as the input.
#     # audio_padded = F.pad(audio_batch.unsqueeze(1), (0, ir_length - 1))
#     audio_padded = F.pad(audio_batch.unsqueeze(1), (ir_length - 1, 0))
#     convolved = F.conv1d(audio_padded, ir_kernel)

#     # Save the output if an output path is provided (only supported for batch size 1).
#     if output_path is not None:
#         if batch_size != 1:
#             raise ValueError("Saving output audio is only supported for a batch size of 1.")
#         # torchaudio expects shape (channels, n_samples)
#         torchaudio.save(output_path, convolved[0], sr_audio)
#         print(f"Convolved audio saved as '{output_path}'.")

#     # Return the original mono audio and the convolved audio, each with a channel dimension.
#     return audio_batch.unsqueeze(1), convolved, sr_audio


def apply_reverb(*, 
         audio_path: tp.Union[str, None] = None, 
         audio_wav: tp.Union[torch.Tensor, None] = None, 
         audio_wav_sr: tp.Union[int, None] = None,
         ir_path: tp.Union[str, None] = None,
         ir_wav: tp.Union[torch.Tensor, None] = None, 
         ir_wav_sr: tp.Union[int, None] = None,
         output_path: tp.Union[str, None] = None,
         ) -> tp.Tuple[torch.Tensor, torch.Tensor, int]:
    """
    Apply convolution reverb to an audio file or tensor using torch.nn.functional.conv1d.

    The audio input can be provided as either:
      - A tensor of shape (n_channels, n_samples) (single example), or
      - A tensor of shape (batch_size, n_channels, n_samples).
      
    In the single-example case the tensor is automatically unsqueezed to add a batch dimension.

    Args:
        audio_path: Path to the input audio file.
        audio_wav: Input audio as a torch.Tensor (n_channels, n_samples) or (batch_size, n_channels, n_samples).
        audio_wav_sr: Sampling rate of the input audio.
        ir_path: Path to the impulse response file.
        ir_wav: Impulse response as a torch.Tensor (n_channels, n_samples).
        ir_wav_sr: Sampling rate of the impulse response.
        output_path: Path where the output audio will be saved.
        use_partitioned: If True, processes the audio in blocks (overlap‑add) to reduce memory usage.
        block_size: Block size (in samples) to use for partitioned convolution. If not provided and 
                    use_partitioned is True, defaults to 10 seconds of audio (sr_audio * 10).
                    
    Returns:
        Tuple containing:
        - Original mono audio waveform (torch.Tensor) with shape (batch_size, 1, n_samples)
        - Convolved audio waveform (torch.Tensor) with shape (batch_size, 1, n_samples)
        - Sample rate (int)
    """
    # Validate audio input
    if audio_path is None and audio_wav is None:
        raise ValueError("Either audio_path or audio_wav must be provided.")
    if isinstance(audio_path, str) and audio_wav is not None:
        raise ValueError("Only one of audio_path or audio_wav can be provided.")

    # Load audio
    if audio_path is not None:
        audio_waveform, sr_audio = torchaudio.load(audio_path)  # shape: (n_channels, n_samples)
        # Add a batch dimension: (1, n_channels, n_samples)
        audio_waveform = audio_waveform.unsqueeze(0)
    else:
        audio_waveform = audio_wav
        sr_audio = audio_wav_sr
        # If provided as (n_channels, n_samples), unsqueeze to get (1, n_channels, n_samples)
        if audio_waveform.dim() == 2:
            audio_waveform = audio_waveform.unsqueeze(0)
        elif audio_waveform.dim() != 3:
            raise ValueError("audio_wav must be a 2D or 3D tensor.")

    # Load impulse response (IR)
    if ir_path is not None:
        ir_waveform, sr_ir = torchaudio.load(ir_path)  # shape: (n_channels, n_samples)
    else:
        if ir_wav is None:
            raise ValueError("Either ir_path or ir_wav must be provided.")
        ir_waveform, sr_ir = ir_wav, ir_wav_sr
        if ir_waveform.dim() != 2:
            raise ValueError("ir_wav must be a 2D tensor of shape (n_channels, n_samples).")

    # Ensure the sampling rates match; resample IR if needed.
    if sr_audio != sr_ir:
        ir_waveform = torchaudio.functional.resample(ir_waveform, sr_ir, sr_audio)

    # Convert multi-channel audio to mono by averaging channels.
    # For audio_waveform: shape (batch_size, n_channels, n_samples)
    if audio_waveform.shape[1] > 1:
        audio_waveform = audio_waveform.mean(dim=1, keepdim=True)
    # For ir_waveform: shape (n_channels, n_samples)
    if ir_waveform.shape[0] > 1:
        ir_waveform = ir_waveform.mean(dim=0, keepdim=True)
    
    # Remove the channel dimension for further processing and ensure float32.
    # audio_batch: shape (batch_size, n_samples)
    audio_batch = audio_waveform.float()

    # Prepare the impulse response.
    ir = ir_waveform.squeeze(0).float()  # shape: (ir_length,)
    ir_length = ir.numel()
    # Prepare IR kernel for conv1d: shape (1, 1, ir_length)
    ir_kernel = ir.view(1, 1, ir_length)

    # noramlize ir
    # to distribute the energy, making its gain a unit gain.
    # by doing this, the convolution doesn’t attenuate (or amplify) the overall energy of the speech signal.
    ir_kernel = ir_kernel / ir_kernel.norm(p=2)  

    # Process the entire audio at once.
    # # Pad the audio on the right so that conv1d produces an output of the same length as the input.
    # # audio_padded = F.pad(audio_batch.unsqueeze(1), (0, ir_length - 1))
    # audio_padded = F.pad(audio_batch, (ir_length - 1, 0))
    # convolved = F.conv1d(audio_padded, ir_kernel)
    convolved = taF.fftconvolve(audio_batch, ir_kernel)[..., :-ir_length+1]

    # Save the output if an output path is provided (only supported for batch size 1).
    if output_path is not None:
        # if batch_size != 1:
        #     raise ValueError("Saving output audio is only supported for a batch size of 1.")
        # torchaudio expects shape (channels, n_samples)
        torchaudio.save(output_path, convolved[0], sr_audio)
        print(f"Convolved audio saved as '{output_path}'.")

    # Return the original mono audio and the convolved audio, each with a channel dimension.
    return audio_batch, convolved, sr_audio
