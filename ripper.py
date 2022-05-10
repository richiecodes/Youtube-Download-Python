# YouTube Ripper
# Author: Richard DeLuca
# https://www.github.com/richiecodes

import PySimpleGUI as sg
from pytube import YouTube


def progress_check(stream, chunk, bytes_remaining):
    window['-DOWNLOADPROGRESS-'].update(100 -
                                        round(bytes_remaining / stream.filesize * 100))


def on_complete(stream, file_path):
    window['-DOWNLOADPROGRESS-'].update(0)


sg.theme('reddit')

start_layout = [[sg.Text('Youtube Ripper by Richard DeLuca'), sg.Push(), sg.Text(
    'www.github.com/richiecodes', justification='Right Justified')], [sg.Input(key='-INPUT-'), sg.Button('Open')]]

info_tab = [
    [sg.Text('Title:'), sg.Text(key='-TITLE-')],
    [sg.Text('Length:'), sg.Text(key='-LENGTH-')],
    [sg.Text('Views:'), sg.Text(key='-VIEWS-')],
    [sg.Text('Author:'), sg.Text(key='-AUTHOR-')],
    [sg.Text('Description:'), sg.Multiline(key='-DESCRIPTION-',
                                           size=(40, 20), no_scrollbar=True, disabled=True)]
]

download_tab = [
    [sg.Frame('Best Quality', [[sg.Button('Download', key='-BEST-'),
              sg.Text('', key='-BESTRES-'), sg.Text('', key='-BESTSIZE-')]])],
    [sg.Frame('Worst Quality', [[sg.Button('Download', key='-WORST-'),
              sg.Text('', key='-WORSTRES-'), sg.Text('', key='-WORSTSIZE-')]])],
    [sg.Frame('Audio', [[sg.Button('Download', key='-AUDIO-'),
              sg.Text('', key='-AUDIOSIZE-')]])],
    [sg.VPush()],
    [sg.Progress(100, orientation='horizontal', size=(20, 20),
                 key='-DOWNLOADPROGRESS-', expand_x=True)]
]

layout = [[sg.TabGroup([[
    sg.Tab('Info', info_tab), sg.Tab('Download', download_tab)]])]]

window = sg.Window('Youtube Ripper', start_layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    if event == 'Open':
        window.close()
        video_obj = YouTube(
            values['-INPUT-'], on_progress_callback=progress_check, on_complete_callback=on_complete)
        window = sg.Window('Youtube Ripper', layout, finalize=True)
        window['-TITLE-'].update(video_obj.title)
        window['-LENGTH-'].update(f'{round(video_obj.length / 60,2)} minutes')
        window['-VIEWS-'].update(video_obj.views)
        window['-AUTHOR-'].update(video_obj.author)
        window['-DESCRIPTION-'].update(video_obj.description)
        window['-BESTSIZE-'].update(
            f'{round(video_obj.streams.get_highest_resolution().filesize / 1048576,1)} MB')
        window['-BESTRES-'].update(
            video_obj.streams.get_highest_resolution().resolution)

        window['-WORSTSIZE-'].update(
            f'{round(video_obj.streams.get_lowest_resolution().filesize / 1048576,1)} MB')
        window['-WORSTRES-'].update(
            video_obj.streams.get_lowest_resolution().resolution)

        window['-AUDIOSIZE-'].update(
            f'{round(video_obj.streams.get_audio_only().filesize / 1048576,1)} MB')

    if event == '-BEST-':
        video_obj.streams.get_highest_resolution().download()

    if event == '-WORST-':
        video_obj.streams.get_lowest_resolution().download()

    if event == '-AUDIO-':
        video_obj.streams.get_audio_only().download()

window.close()
