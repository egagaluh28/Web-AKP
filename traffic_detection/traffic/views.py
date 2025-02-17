from django.shortcuts import render, redirect
from .forms import TrafficForm
from .models import TrafficData
import cv2
import numpy as np
import yt_dlp as youtube_dl
import os

def traffic_form(request):
    if request.method == 'POST':
        form = TrafficForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('traffic_data')
    else:
        form = TrafficForm()
    return render(request, 'traffic/form.html', {'form': form})

def traffic_data(request):
    data = TrafficData.objects.all()
    return render(request, 'traffic/data.html', {'data': data})

def detect_traffic_density(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        return 0

    # Contoh sederhana: hitung jumlah piksel yang bergerak
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    first_frame = gray

    density = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        delta_frame = cv2.absdiff(first_frame, gray)
        thresh_frame = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

        contours, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue
            density += 1

        first_frame = gray

    cap.release()
    return density

def traffic_density_view(request):
    video_url = 'https://youtu.be/8FRW8RQfEeI?si=zDplMPQFWHct9YFT'  # Ganti dengan URL video YouTube Anda

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'D:/fortofolio/coding/web pythone/traffic_detection/%(title)s.%(ext)s',  # Ganti dengan path direktori unduhan Anda
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        video_path = ydl.prepare_filename(info_dict)

    density = detect_traffic_density(video_path)

    # Hapus video setelah selesai diproses
    os.remove(video_path)

    return render(request, 'traffic/density.html', {'density': density})