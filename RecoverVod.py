import datetime
import hashlib
import os
import random
import re
from datetime import timedelta
import grequests
import requests
from bs4 import BeautifulSoup
from moviepy.editor import concatenate_videoclips, VideoFileClip
from natsort import natsorted

domains = ["https://vod-secure.twitch.tv/",
           "https://vod-metro.twitch.tv/",
           "https://vod-pop-secure.twitch.tv/",
           "https://d2e2de1etea730.cloudfront.net/",
           "https://dqrpb9wgowsf5.cloudfront.net/",
           "https://ds0h3roq6wcgc.cloudfront.net/",
           "https://d2nvs31859zcd8.cloudfront.net/",
           "https://d2aba1wr3818hz.cloudfront.net/",
           "https://d3c27h4odz752x.cloudfront.net/",
           "https://dgeft87wbj63p.cloudfront.net/",
           "https://d1m7jfoe9zdc1j.cloudfront.net/",
           "https://d3vd9lfkzbru3h.cloudfront.net/",
           "https://d2vjef5jvl6bfs.cloudfront.net/",
           "https://d1ymi26ma8va5x.cloudfront.net/",
           "https://d1mhjrowxxagfy.cloudfront.net/",
           "https://ddacn6pr5v0tl.cloudfront.net/",
           "https://d3aqoihi2n8ty8.cloudfront.net/"]

user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.5; rv:103.0) Gecko/20100101 Firefox/103.0",
               "Mozilla/5.0 (X11; Linux i686; rv:103.0) Gecko/20100101 Firefox/103.0",
               "Mozilla/5.0 (Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
               "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:103.0) Gecko/20100101 Firefox/103.0",
               "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
               "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.5; rv:102.0) Gecko/20100101 Firefox/102.0",
               "Mozilla/5.0 (X11; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0",
               "Mozilla/5.0 (Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
               "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0",
               "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
               "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 Edg/103.0.1264.77",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 Edg/103.0.1264.77",
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36']


def print_main_menu():
    menu = "1) Recover Vod" + "\n" + "2) Recover Clips" + "\n" + "3) Unmute an M3U8 file" + "\n" + "4) Check M3U8 Segments" + "\n" + "5) Generate M3U8 file (ONLY includes valid segments)" + "\n" + "6) Download M3U8 (.MP4 extension)" + "\n" + "7) Exit" + "\n"
    print(menu)


def print_vod_type_menu():
    vod_type_menu = "Enter what type of vod recovery: " + "\n" + "1) Recover Vod" + "\n" + "2) Recover vods from SullyGnome CSV export" + "\n" + "3) Exit" + "\n"
    print(vod_type_menu)


def print_vod_recovery_menu():
    vod_recovery_method = "Enter vod recovery method: " + "\n" + "1) Manual Vod Recover" + "\n" + "2) Website Vod Recover" + "\n" + "3) Exit" + "\n"
    print(vod_recovery_method)


def print_clip_type_menu():
    clip_type_menu = "Enter what type of clip recovery: " + "\n" + "1) Recover all clips from a single VOD" + "\n" + "2) Find random clips from a single VOD" + "\n" + "3) Bulk recover clips from SullyGnome CSV export" + "\n" + "4) Exit" + "\n"
    print(clip_type_menu)


def print_clip_recovery_menu():
    clip_recovery_method = "Enter clip recovery method: " + "\n" + "1) Manual Clip Recover" + "\n" + "2) Website Clip Recover" + "\n" + "3) Exit" + "\n"
    print(clip_recovery_method)


def print_clip_format_menu():
    clip_format_menu = "What clip url format would you like to use (delimited by spaces)? " + "\n" + "1) Default ([VodID]-offset-[interval])" + "\n" + "2) Alternate Format (vod-[VodID]-offset-[interval])" + "\n" + "3) Legacy ([VodID]-index-[interval])" + "\n"
    print(clip_format_menu)


def get_default_directory():
    return os.path.expanduser("~/Documents/")


def generate_log_filename(streamer, vod_id):
    log_filename = os.path.join(get_default_directory(), streamer + "_" + vod_id + "_log.txt")
    return log_filename


def generate_vod_filename(streamer, vod_id):
    vod_filename = os.path.join(get_default_directory(), "VodRecovery_" + streamer + "_" + vod_id + ".m3u8")
    return vod_filename


def generate_website_links(streamer, vod_id):
    website_list = ["https://sullygnome.com/channel/" + streamer + "/stream/" + vod_id,
                    "https://twitchtracker.com/" + streamer + "/streams/" + vod_id,
                    "https://streamscharts.com/channels/" + streamer + "/streams/" + vod_id]

    return website_list


def return_header():
    header = {
        'user-agent': f'{random.choice(user_agents)}'
    }
    return header


def remove_file(file_path):
    if os.path.exists(file_path):
        return os.remove(file_path)


def format_timestamp(timestamp):
    formatted_date = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return formatted_date


def get_vod_age(timestamp):
    vod_age = datetime.datetime.today() - format_timestamp(timestamp)
    if vod_age.days <= 0:
        return 0
    else:
        return vod_age.days


def is_vod_muted(url):
    return bool("unmuted" in requests.get(url).text)


def get_duration(hours, minutes):
    return (int(hours) * 60) + int(minutes)


def get_reps(duration):
    reps = ((duration * 60) + 2000)
    return reps


def get_clip_format(vod_id, reps):
    default_clip_list = ["https://clips-media-assets2.twitch.tv/" + vod_id + "-offset-" + str(i) + ".mp4" for i in
                         range(reps) if i % 2 == 0]

    alternate_clip_list = ["https://clips-media-assets2.twitch.tv/vod-" + vod_id + "-offset-" + str(i) + ".mp4" for i in
                           range(reps) if i % 2 == 0]

    legacy_clip_list = [
        "https://clips-media-assets2.twitch.tv/" + vod_id + "-index-" + "%010g" % (int('000000000') + i) + ".mp4" for i
        in range(reps)]

    clip_format_dict = {}

    clip_format_dict.update({"1": default_clip_list})
    clip_format_dict.update({"2": alternate_clip_list})
    clip_format_dict.update({"3": legacy_clip_list})

    return clip_format_dict


def get_all_clip_urls(clip_dict, clip_format):
    full_url_list = []
    for key, value in clip_dict.items():
        if key in clip_format:
            full_url_list += value
    return full_url_list


def return_username(url):
    indices = [i.start() for i in re.finditer('_', url)]
    username = url[indices[0] + 1:indices[-2]]
    return username


def return_vod_id(url):
    indices = [i.start() for i in re.finditer('_', url)]
    vod_id = url[indices[0] + len(return_username(url)) + 2:indices[-1]]
    return vod_id


def remove_chars_from_ordinal_numbers(datetime_string):
    ordinal_array = ["th", "nd", "st", "rd"]
    for exclude_string in ordinal_array:
        if exclude_string in datetime_string:
            return datetime_string.replace(datetime_string.split(" ")[1], datetime_string.split(" ")[1][:-len(exclude_string)])


def return_file_contents(streamer, vod_id):
    with open(generate_log_filename(streamer, vod_id)) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
    return content


def get_vod_urls(streamer, vod_id, timestamp):
    vod_url_list, valid_vod_url_list = [], []
    for seconds in range(60):
        epoch_timestamp = ((format_timestamp(timestamp) + timedelta(seconds=seconds)) - datetime.datetime(1970, 1,
                                                                                                          1)).total_seconds()
        base_url = streamer + "_" + vod_id + "_" + str(int(epoch_timestamp))
        hashed_base_url = str(hashlib.sha1(base_url.encode('utf-8')).hexdigest())[:20]
        for domain in domains:
            vod_url_list.append(domain + hashed_base_url + "_" + base_url + "/chunked/index-dvr.m3u8")
    request_session = requests.Session()
    rs = [grequests.head(u, session=request_session) for u in vod_url_list]
    for result in grequests.imap(rs, size=100):
        if result.status_code == 200:
            valid_vod_url_list.append(result.url)
    return valid_vod_url_list


def parse_duration_streamscharts(tracker_url):
    for _ in range(10):
        response = requests.get(tracker_url, headers=return_header(), allow_redirects=False)
        if response.status_code == 200:
            bs = BeautifulSoup(response.content, 'html.parser')
            streamscharts_duration = bs.find_all('div', {'class': 'text-xs font-bold'})[3].text.strip().replace("h", "").replace("m", "").split(" ")
            return get_duration(int(streamscharts_duration[0]), int(streamscharts_duration[1]))


def parse_duration_twitchtracker(tracker_url):
    response = requests.get(tracker_url, headers=return_header(), allow_redirects=False)
    if response.status_code == 200:
        bs = BeautifulSoup(response.content, 'html.parser')
        twitchtracker_duration = bs.find_all('div', {'class': 'g-x-s-value'})[0].text
        return twitchtracker_duration


def parse_duration_sullygnome(tracker_url):
    response = requests.get(tracker_url, headers=return_header(), allow_redirects=False)
    if response.status_code == 200:
        bs = BeautifulSoup(response.content, 'html.parser')
        sullygnome_duration = bs.find_all('div', {'class': 'MiddleSubHeaderItemValue'})[7].text.strip().replace("hours", "").replace("minutes", "").split(",")
        return get_duration(int(sullygnome_duration[0]), int(sullygnome_duration[1]))


def parse_datetime_streamscharts(tracker_url):
    for _ in range(10):
        response = requests.get(tracker_url, headers=return_header(), allow_redirects=False)
        if response.status_code == 200:
            bs = BeautifulSoup(response.content, 'html.parser')
            streamscharts_datetime = bs.find_all('time', {'class': 'ml-2 font-bold'})[0].text.strip().replace(",", "") + ":00"
            return datetime.datetime.strftime(datetime.datetime.strptime(streamscharts_datetime, "%d %b %Y %H:%M:%S"), "%Y-%m-%d %H:%M:%S")


def parse_datetime_twitchtracker(tracker_url):
    response = requests.get(tracker_url, headers=return_header(), allow_redirects=False)
    bs = BeautifulSoup(response.content, 'html.parser')
    twitchtracker_datetime = bs.find_all('div', {'class': 'stream-timestamp-dt'})[0].text
    return twitchtracker_datetime


def parse_datetime_sullygnome(tracker_url):
    response = requests.get(tracker_url, headers=return_header(), allow_redirects=False)
    bs = BeautifulSoup(response.content, 'html.parser')
    stream_date = bs.find_all('div', {'class': 'MiddleSubHeaderItemValue'})[6].text
    modified_stream_date = remove_chars_from_ordinal_numbers(stream_date)
    formatted_stream_date = datetime.datetime.strftime(datetime.datetime.strptime(modified_stream_date, "%A %d %B %I:%M%p"), "%m-%d %H:%M:%S")
    return str(datetime.datetime.now().year) + "-" + formatted_stream_date


def unmute_vod(url):
    file_contents = []
    counter = 0
    vod_file_path = generate_vod_filename(return_username(url), return_vod_id(url))
    with open(vod_file_path, "w") as vod_file:
        vod_file.write(requests.get(url, stream=True).text)
    vod_file.close()
    with open(vod_file_path, "r") as vod_file:
        for lines in vod_file.readlines():
            file_contents.append(lines)
    vod_file.close()
    with open(vod_file_path, "w") as vod_file:
        for segment in file_contents:
            url = url.replace("index-dvr.m3u8", "")
            if "-unmuted" in segment and not segment.startswith("#"):
                counter += 1
                vod_file.write(segment.replace(segment, str(url) + str(counter - 1)) + "-muted.ts" + "\n")
            elif "-unmuted" not in segment and not segment.startswith("#"):
                counter += 1
                vod_file.write(segment.replace(segment, str(url) + str(counter - 1)) + ".ts" + "\n")
            else:
                vod_file.write(segment)
    vod_file.close()
    print(os.path.basename(vod_file_path) + " Has been unmuted!")


def dump_playlist(url):
    file_contents = []
    counter = 0
    vod_file_path = generate_vod_filename(return_username(url), return_vod_id(url))
    with open(vod_file_path, "w") as vod_file:
        vod_file.write(requests.get(url, stream=True).text)
    vod_file.close()
    with open(vod_file_path, "r") as vod_file:
        for lines in vod_file.readlines():
            file_contents.append(lines)
    vod_file.close()
    with open(vod_file_path, "w") as vod_file:
        for segment in file_contents:
            url = url.replace("index-dvr.m3u8", "")
            if not segment.startswith("#"):
                counter += 1
                vod_file.write(segment.replace(segment, str(url) + str(counter - 1)) + ".ts" + "\n")
            else:
                vod_file.write(segment)
    vod_file.close()


def return_valid_file(url):
    if is_vod_muted(url):
        print("Vod contains muted segments")
        unmute_vod(url)
    else:
        print("Vod does NOT contain muted segments")
        dump_playlist(url)
    new_playlist = []
    vod_file_path = generate_vod_filename(return_username(url), return_vod_id(url))
    new_vod_file_path = generate_vod_filename(return_username(url), return_vod_id(url) + "_MODIFIED")
    lines = open(vod_file_path, "r+").read().splitlines()
    segments = get_valid_segments(get_all_playlist_segments(url))
    if len(segments) < 1:
        print("No segments are valid.. Cannot generate M3U8! Returning to main menu.")
        remove_file(vod_file_path)
        return
    new_playlist_segments = [x for x in segments if x in lines]
    for segment in natsorted(new_playlist_segments):
        for line in lines:
            if line == segment:
                new_playlist.append(segment)
            if line != segment and line.startswith("#"):
                new_playlist.append(line)
            elif line.endswith(".ts") and segment not in new_playlist and not line.startswith("#"):
                line = "#" + line
                new_playlist.append(line)
            else:
                if line not in new_playlist:
                    new_playlist.append(line)
        break
    with open(new_vod_file_path, "a+") as new_vod_file:
        for playlist_lines in new_playlist:
            new_vod_file.write(playlist_lines + "\n")
    new_vod_file.close()
    remove_file(vod_file_path)


def get_all_playlist_segments(url):
    counter = 0
    file_contents, segment_list = [], []
    vod_file_path = generate_vod_filename(return_username(url), return_vod_id(url))
    with open(vod_file_path, "w") as vod_file:
        vod_file.write(requests.get(url, stream=True).text)
    vod_file.close()
    with open(vod_file_path, "r") as vod_file:
        for lines in vod_file.readlines():
            file_contents.append(lines)
    vod_file.close()
    with open(vod_file_path, "w") as vod_file:
        for segment in file_contents:
            url = url.replace("index-dvr.m3u8", "")
            if "-unmuted" in segment and not segment.startswith("#"):
                counter += 1
                vod_file.write(segment.replace(segment, str(url) + str(counter - 1)) + "-muted.ts" + "\n")
                segment_list.append(str(url) + str(counter - 1) + "-muted.ts")
            elif "-unmuted" not in segment and not segment.startswith("#"):
                counter += 1
                vod_file.write(segment.replace(segment, str(url) + str(counter - 1)) + ".ts" + "\n")
                segment_list.append(str(url) + str(counter - 1) + ".ts")
            else:
                vod_file.write(segment)
    vod_file.close()
    return segment_list


def get_valid_segments(segments):
    valid_segment_counter, current_count = 0, 0
    all_segments, valid_segments = [], []
    for url in segments:
        all_segments.append(url.strip())
    request_session = requests.Session()
    rs = [grequests.head(u, session=request_session) for u in all_segments]
    for result in grequests.imap(rs, size=100):
        current_count += 1
        progress_percentage = (current_count * 100) // len(all_segments)
        if current_count == len(all_segments):
            print("\rChecking segment ", current_count, "/", len(all_segments), "... (progress : ", progress_percentage, "%)", sep='')
        else:
            print("\rChecking segment ", current_count, "/", len(all_segments), "... (progress : ", progress_percentage, "%)", sep='', end='')
        if result.status_code == 200:
            valid_segment_counter += 1
            valid_segments.append(result.url)
    return valid_segments


def return_segment_ratio(url):
    segment_string = str(len(get_valid_segments(get_all_playlist_segments(url)))) + " of " + str(
        len(get_all_playlist_segments(url))) + " Segments are valid"
    print(segment_string)


def vod_recover(streamer, vod_id, timestamp):
    print("Vod is " + str(get_vod_age(timestamp)) + " days old. If the vod is older than 60 days chances of recovery are slim." + "\n")
    vod_url_list = get_vod_urls(streamer, vod_id, timestamp)
    if len(vod_url_list) > 0:
        vod_url = random.choice(vod_url_list)
        if is_vod_muted(vod_url):
            print(vod_url + "\n" + "Vod contains muted segments")
            user_input = input("Would you like to unmute the vod (Y/N): ")
            if user_input.upper() == "Y":
                unmute_vod(vod_url)
                print("Total Number of Segments: " + str(len(get_all_playlist_segments(vod_url))))
                user_option = input("Would you like to check if segments are valid (Y/N): ")
                if user_option.upper() == "Y":
                    return_segment_ratio(vod_url)
                else:
                    return
            else:
                return
        else:
            print(vod_url + "\n" + "Vod does NOT contain muted segments")
            print("Total Number of Segments: " + str(len(get_all_playlist_segments(vod_url))))
            user_option = input("Would you like to check if segments are valid (Y/N): ")
            if user_option.upper() == "Y":
                return_segment_ratio(vod_url)
            else:
                return
    else:
        print(
            "No vods found using current domain list. " + "\n" + "See the following links if you would like to check the other sites: " + "\n")
        for website in generate_website_links(streamer, vod_id):
            print(website)


def manual_vod_recover():
    streamer = input("Enter streamer name: ")
    vod_id = input("Enter vod id: ")
    timestamp = input("Enter VOD start time (YYYY-MM-DD HH:MM:SS): ")
    vod_recover(streamer, vod_id, timestamp)


def website_vod_recover():
    tracker_url = input("Enter twitchtracker/streamscharts/sullygnome url:  ")
    if "streamscharts" in tracker_url:
        streamer = tracker_url.split("channels/", 1)[1].split("/")[0]
        vod_id = tracker_url.split("streams/", 1)[1]
        vod_recover(streamer, vod_id, parse_datetime_streamscharts(tracker_url))
    elif "twitchtracker" in tracker_url:
        streamer = tracker_url.split("com/", 1)[1].split("/")[0]
        vod_id = tracker_url.split("streams/", 1)[1]
        vod_recover(streamer, vod_id, parse_datetime_twitchtracker(tracker_url))
    elif "sullygnome" in tracker_url:
        streamer = tracker_url.split("channel/", 1)[1].split("/")[0]
        vod_id = tracker_url.split("stream/", 1)[1]
        vod_recover(streamer, vod_id, parse_datetime_sullygnome(tracker_url))
    else:
        print("Link not supported.. Returning to main menu.")
        return


def website_clip_recover():
    tracker_url = input("Enter twitchtracker/streamscharts/sullygnome url:  ")
    if "streamscharts" in tracker_url:
        streamer = tracker_url.split("channels/", 1)[1].split("/")[0]
        vod_id = tracker_url.split("streams/", 1)[1]
        clip_recover(streamer, vod_id, int(parse_duration_streamscharts(tracker_url)))
    elif "twitchtracker" in tracker_url:
        streamer = tracker_url.split("com/", 1)[1].split("/")[0]
        vod_id = tracker_url.split("streams/", 1)[1]
        clip_recover(streamer, vod_id, int(parse_duration_twitchtracker(tracker_url)))
    elif "sullygnome" in tracker_url:
        streamer = tracker_url.split("channel/", 1)[1].split("/")[0]
        vod_id = tracker_url.split("stream/", 1)[1]
        clip_recover(streamer, vod_id, int(parse_duration_sullygnome(tracker_url)))
    else:
        print("Link not supported.. Returning to main menu.")
        return


def bulk_vod_recovery():
    streamer = input("Enter streamer name: ")
    file_path = input("Enter full path of sullygnome CSV file: ").replace('"', '')
    for timestamp, vod_id in parse_vod_csv_file(file_path).items():
        print("\n" + "Recovering Vod....", vod_id)
        vod_url_list = get_vod_urls(streamer, vod_id, timestamp)
        if len(vod_url_list) > 0:
            vod_url = random.choice(vod_url_list)
            if is_vod_muted(vod_url):
                print(vod_url + "\n" + "Vod contains muted segments")
            else:
                print(vod_url + "\n" + "Vod does NOT contain muted segments")
        else:
            print("No vods found using current domain list." + "\n")


def clip_recover(streamer, vod_id, duration):
    total_counter, iteration_counter, valid_counter = 0, 0, 0
    valid_url_list = []
    print_clip_format_menu()
    clip_format = input("Please choose an option: ").split(" ")
    full_url_list = get_all_clip_urls(get_clip_format(vod_id, get_reps(duration)), clip_format)
    request_session = requests.Session()
    rs = [grequests.head(u, session=request_session) for u in full_url_list]
    for result in grequests.imap(rs, size=100):
        total_counter += 1
        iteration_counter += 1
        if total_counter == 500:
            print(str(iteration_counter) + " of " + str(len(full_url_list)))
            total_counter = 0
        if result.status_code == 200:
            valid_counter += 1
            valid_url_list.append(result.url)
            print(str(valid_counter) + " Clip(s) Found")
    if len(valid_url_list) >= 1:
        with open(generate_log_filename(streamer, vod_id), "w") as log_file:
            for url in valid_url_list:
                log_file.write(url + "\n")
        log_file.close()
        download_option = input("Do you want to download the recovered clips (Y/N): ")
        if download_option.upper() == "Y":
            download_clips(get_default_directory(), streamer, vod_id)
            keep_log_option = input("Do you want to remove the log file? ")
            if keep_log_option.upper() == "Y":
                remove_file(generate_log_filename(streamer, vod_id))
            else:
                pass
        else:
            return
    else:
        print("No clips found! Returning to main menu.")
        return


def manual_clip_recover():
    streamer = input("Enter streamer name: ")
    vod_id = input("Enter vod id: ")
    hours = input("Enter stream duration hour value: ")
    minutes = input("Enter stream duration minute value: ")
    clip_recover(streamer, vod_id, get_duration(hours, minutes))


def parse_clip_csv_file(file_path):
    vod_info_dict = {}
    csv_file = open(file_path, "r+")
    lines = csv_file.readlines()[1:]
    for line in lines:
        if line.strip():
            filtered_string = line.partition("stream/")[2].replace('"', "")
            vod_id = filtered_string.split(",")[0]
            duration = filtered_string.split(",")[1]
            if vod_id != 0:
                reps = get_reps(int(duration))
                vod_info_dict.update({vod_id: reps})
            else:
                pass
    csv_file.close()
    return vod_info_dict


def parse_vod_csv_file(file_path):
    vod_info_dict = {}
    csv_file = open(file_path, "r+")
    lines = csv_file.readlines()[1:]
    for line in lines:
        if line.strip():
            modified_stream_date = remove_chars_from_ordinal_numbers(line.split(",")[1].replace('"', ""))
            stream_date = datetime.datetime.strftime(datetime.datetime.strptime(modified_stream_date, "%A %d %B %Y %H:%M"), "%Y-%m-%d %H:%M:%S")
            vod_id = line.partition("stream/")[2].split(",")[0].replace('"', "")
            vod_info_dict.update({stream_date: vod_id})
    csv_file.close()
    return vod_info_dict


def get_random_clips():
    counter = 0
    vod_id = input("Enter vod id: ")
    hours = input("Enter stream duration hour value: ")
    minutes = input("Enter stream duration minute value: ")
    print_clip_format_menu()
    clip_format = input("Please choose an option: ").split(" ")
    full_url_list = get_all_clip_urls(get_clip_format(vod_id, get_reps(get_duration(hours, minutes))), clip_format)
    random.shuffle(full_url_list)
    print("Total Number of Urls: " + str(len(full_url_list)))
    request_session = requests.Session()
    rs = [grequests.head(u, session=request_session) for u in full_url_list]
    for result in grequests.imap(rs, size=100):
        if result.status_code == 200:
            counter += 1
            if counter == 1:
                print(result.url)
                user_option = input("Do you want another url (Y/N): ")
                if user_option.upper() == "Y":
                    continue
                else:
                    return
        counter = 0


def bulk_clip_recovery():
    vod_counter, total_counter, valid_counter, iteration_counter = 0, 0, 0, 0
    streamer = input("Enter streamer name: ")
    file_path = input("Enter full path of sullygnome CSV file: ").replace('"', '')
    user_option = input("Do you want to download all clips recovered (Y/N)? ")
    print_clip_format_menu()
    clip_format = input("Please choose an option: ").split(" ")
    for vod_id, duration in parse_clip_csv_file(file_path).items():
        vod_counter += 1
        print("Processing Twitch Vod... " + str(vod_id) + " - " + str(vod_counter) + " of " + str(
            len(parse_clip_csv_file(file_path))))
        original_vod_url_list = get_all_clip_urls(get_clip_format(vod_id, duration), clip_format)
        request_session = requests.Session()
        rs = [grequests.head(u, session=request_session) for u in original_vod_url_list]
        for result in grequests.imap(rs, size=100):
            total_counter += 1
            iteration_counter += 1
            if total_counter == 500:
                print(str(iteration_counter) + " of " + str(len(original_vod_url_list)))
                total_counter = 0
            if result.status_code == 200:
                valid_counter += 1
                print(str(valid_counter) + " Clip(s) Found")
                with open(generate_log_filename(streamer, vod_id), "a+") as log_file:
                    log_file.write(result.url + "\n")
                log_file.close()
            else:
                continue
        if valid_counter != 0:
            if user_option.upper() == "Y":
                download_clips(get_default_directory(), streamer, vod_id)
                remove_file(generate_log_filename(streamer, vod_id))
            else:
                print("Recovered clips logged to " + generate_log_filename(streamer, vod_id))
        total_counter, valid_counter, iteration_counter = 0, 0, 0


def download_m3u8(url):
    os.system("ffmpeg.exe -i \"{}\" -c copy -bsf:a aac_adtstoasc \"{}.mp4\"".format(url, generate_vod_filename(return_username(url), return_vod_id(url)).removesuffix(".m3u8")))


def download_clips(directory, streamer, vod_id):
    counter = 0
    print("Starting Download....")
    download_directory = os.path.join(directory, streamer.title() + "_" + vod_id)
    if os.path.exists(download_directory):
        pass
    else:
        os.mkdir(download_directory)
    for links in return_file_contents(streamer, vod_id):
        counter = counter + 1
        if "-offset-" in links:
            clip_offset = links.split("-offset-")[1].replace(".mp4", "")
        else:
            clip_offset = links.split("-index-")[1].replace(".mp4", "")
        link_url = os.path.basename(links)
        r = requests.get(links, stream=True)
        if r.status_code == 200:
            if str(link_url).endswith(".mp4"):
                with open(os.path.join(download_directory, streamer.title() + "_" + str(vod_id) + "_" + str(
                        clip_offset)) + ".mp4", 'wb') as x:
                    print(datetime.datetime.now().strftime("%Y/%m/%d %I:%M:%S    ") + "Downloading... Clip " + str(
                        counter) + " of " + str(len(return_file_contents(streamer, vod_id))) + " - " + links)
                    x.write(r.content)
            else:
                print("ERROR: Please check the log file and failing link!", links)
        else:
            print("ERROR: " + str(r.status_code) + " - " + str(r.reason))
            pass


def run_script():
    print("WELCOME TO VOD RECOVERY" + "\n")
    menu = 0
    while menu < 7:
        print_main_menu()
        menu = int(input("Please choose an option: "))
        if menu == 7:
            exit()
        elif menu == 1:
            print_vod_type_menu()
            vod_type = int(input("Please choose an option: "))
            if vod_type == 1:
                print_vod_recovery_menu()
                vod_recovery_method = int(input("Please choose an option: "))
                if vod_recovery_method == 1:
                    manual_vod_recover()
                elif vod_recovery_method == 2:
                    website_vod_recover()
                elif vod_recovery_method == 3:
                    exit()
                else:
                    print("Invalid option returning to main menu.")
            elif vod_type == 2:
                bulk_vod_recovery()
            elif vod_type == 3:
                exit()
            else:
                print("Invalid option! Returning to main menu.")
        elif menu == 2:
            print_clip_type_menu()
            clip_type = int(input("Please choose an option: "))
            if clip_type == 1:
                print_clip_recovery_menu()
                clip_recovery_method = int(input("Please choose an option: "))
                if clip_recovery_method == 1:
                    manual_clip_recover()
                elif clip_recovery_method == 2:
                    website_clip_recover()
                elif clip_recovery_method == 3:
                    exit()
                else:
                    print("Invalid option returning to main menu.")
            elif clip_type == 2:
                get_random_clips()
            elif clip_type == 3:
                bulk_clip_recovery()
            elif clip_type == 4:
                exit()
            else:
                print("Invalid option! Returning to main menu.")
        elif menu == 3:
            url = input("Enter M3U8 Link: ")
            if is_vod_muted(url):
                unmute_vod(url)
            else:
                print("Vod does NOT contain muted segments")
        elif menu == 4:
            url = input("Enter M3U8 Link: ")
            return_segment_ratio(url)
            remove_file(generate_vod_filename(return_username(url), return_vod_id(url)))
        elif menu == 5:
            url = input("Enter M3U8 Link: ")
            return_valid_file(url)
        elif menu == 6:
            url = input("Enter M3U8 Link: ")
            download_m3u8(url)
        else:
            print("Invalid Option! Exiting...")


run_script()
