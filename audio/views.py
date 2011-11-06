from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from models import Song
from tasks import ScanMediaTask
from util import send_data, send_file
import os


def scan_media(request):
    ScanMediaTask.delay(r"U:\Music")
    return HttpResponse("Started")

def list_songs(request):
    response = HttpResponse()
    songs = Song.objects.all()
    return render_to_response(
        "library.html",
        {"songs": songs, "count": songs.count()}
    )

def delete_songs(request):
    Song.objects.all().delete()
    return HttpResponse("Deleted all songs.")

def play_song(request, id):
    song = get_object_or_404(Song, pk=id)
    return render_to_response("player.html", {"song": song})

def stream_song(request, id):
    song = get_object_or_404(Song, pk=id)
    url = "/".join(song.file_path.replace("U:\\Music\\", "").split(os.path.sep))
    print url
    return redirect("http://shoebox.local/music/%s" % url)
