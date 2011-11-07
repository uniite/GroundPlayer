from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
import ujson
from models import Song
from tasks import ScanMediaTask
from util import send_data, send_file
import os


def scan_media(request):
    ScanMediaTask.delay(r"U:\Music")
    return HttpResponse("Started")

def library(request):
    return render_to_response("library.html")

def api_songs_count(request):
    return HttpResponse(Song.objects.all().count())

def list_songs(request):
    cache_key = {"view": "audio.views.list_songs"}
    if "sort" in request.GET:
        cache_key["sort"] = request.GET["sort"]
    
    content = cache.get(cache_key)
    if content:
        print "Cache hit"
        return HttpResponse(content)
    else:
        print "Cache miss"
        if "sort" in request.GET:
            songs = Song.objects.all().exclude(title="").order_by(request.GET["sort"])
        else:
            songs = Song.objects.all().exclude(title="")
        content = render(request,
            "song_list.html",
            {"songs": songs, "cache_key": cache_key}
        )
        #cache.set(cache_key, content)
        return HttpResponse(content)

def api_songs_list(request):
    query = Song.objects.all()
    if "sort" in request.GET:
        sort = request.GET["sort"]
        query = query.exclude(**{sort.replace("-", ""): ""}).order_by(sort)
    count = query.count()
    songs = []
    columns = ["title", "artist", "album", "bitrate"]
    for song in query:
        row = [song.pk]
        for attr in columns:
            if attr == "bitrate":
                row.append("%skbps" % getattr(song, attr))
            else:
                row.append(getattr(song, attr))
        songs.append(row)

    return HttpResponse(ujson.encode({
        "columns": ["id"] + columns,
        "count": count,
        "rows": songs
    }))

def delete_songs(request):
    Song.objects.all().delete()
    return HttpResponse("Deleted all songs.")

def play_song(request, id):
    song = get_object_or_404(Song, pk=id)
    return render_to_response("player.html", {"song": song})

def stream_song(request, id):
    song = get_object_or_404(Song, pk=id)
    url = "/".join(song.file_path.replace("U:\\Music\\", "").split(os.path.sep))
    url = url.replace(".flac", ".wav")
    return redirect("http://shoebox.local/music/%s" % url)
