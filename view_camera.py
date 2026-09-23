#!/usr/bin/env python3
"""
CrazySim Camera Viewer (Tkinter/PIL version)
Connects to crazysim.py TCP/UDP video streams and displays them.
Uses Tkinter and Pillow to avoid OpenCV/NumPy version conflicts.
"""

import socket
import struct
import argparse
import tkinter as tk
from PIL import Image, ImageTk

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent', type=int, default=0, help='Agent ID to view camera for')
    parser.add_argument('--port', type=int, default=None, help='Override base UDP port')
    args = parser.parse_args()

    port = args.port if args.port is not None else (5200 + args.agent)
    
    print(f"Connecting to Agent {args.agent} camera stream on UDP port {port}...")
    
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))
    sock.setblocking(False)
    
    print(f"Waiting for camera frames... (Ensure simulation is running with --camera)")

    # Setup Tkinter UI
    root = tk.Tk()
    root.title(f"Agent {args.agent} Camera")
    root.geometry("648x488")
    
    label = tk.Label(root)
    label.pack(expand=True, fill="both")

    # Reassembly buffers
    frame_chunks = {}
    expected_chunks = -1
    img_width = 0
    img_height = 0

    def update_frame():
        nonlocal expected_chunks, img_width, img_height, frame_chunks
        
        try:
            # Read all available packets
            while True:
                data, addr = sock.recvfrom(65507)
                if len(data) < 8:
                    continue
                    
                # Header format: <HHHH (seq, total, width, height)
                seq, total, width, height = struct.unpack('<HHHH', data[:8])
                chunk_data = data[8:]
                
                # If we receive a new frame's first chunk (or if total changed)
                if expected_chunks != total:
                    frame_chunks.clear()
                    expected_chunks = total
                    img_width = width
                    img_height = height
                    
                frame_chunks[seq] = chunk_data
                
                # If we have all chunks for a frame
                if len(frame_chunks) == expected_chunks and expected_chunks > 0:
                    # Reassemble
                    frame_bytes = bytearray()
                    for i in range(expected_chunks):
                        frame_bytes.extend(frame_chunks.get(i, b''))
                    
                    # Check length
                    expected_len = img_width * img_height
                    if len(frame_bytes) >= expected_len:
                        # Convert to PIL Image (grayscale 'L')
                        img = Image.frombytes('L', (img_width, img_height), bytes(frame_bytes[:expected_len]))
                        # Scale up 2x
                        img = img.resize((img_width * 2, img_height * 2), Image.NEAREST)
                        
                        # Display
                        photo = ImageTk.PhotoImage(image=img)
                        label.config(image=photo)
                        label.image = photo # Keep a reference!
                            
                    # Clear for next frame
                    frame_chunks.clear()
                    
        except BlockingIOError:
            pass # No more packets right now
        except Exception as e:
            print(f"Error receiving frame: {e}")
            
        # Schedule next update
        root.after(10, update_frame)

    # Start the update loop
    root.after(10, update_frame)
    
    # Handle 'q' to quit
    root.bind('q', lambda e: root.destroy())
    
    root.mainloop()
    sock.close()

if __name__ == "__main__":
    main()
