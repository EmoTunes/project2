# if mood < 0.10:
#     if (0 <= track_data["valence"] <= (mood + 0.15)
#         and track_data["danceability"] <= (mood*8)
#             and track_data["energy"] <= (mood*10)):
#         selected_tracks_uri.append(track_data["uri"])
# elif 0.10 <= mood < 0.25:
#     if ((mood - 0.075) <= track_data["valence"] <= (mood + 0.075)
#         and track_data["danceability"] <= (mood*4)
#             and track_data["energy"] <= (mood*5)):
#         selected_tracks_uri.append(track_data["uri"])
# elif 0.25 <= mood < 0.50:
#     if ((mood - 0.085) <= track_data["valence"] <= (mood + 0.085)
#         and track_data["danceability"] <= (mood*3)
#             and track_data["energy"] <= (mood*3.5)):
#         selected_tracks_uri.append(track_data["uri"])
# elif 0.50 <= mood < 0.75:
#     if ((mood - 0.075) <= track_data["valence"] <= (mood + 0.075)
#         and track_data["danceability"] >= (mood/2.5)
#             and track_data["energy"] >= (mood/2)):
#         selected_tracks_uri.append(track_data["uri"])
# elif 0.75 <= mood < 0.90:
#     if ((mood - 0.075) <= track_data["valence"] <= (mood + 0.075)
#         and track_data["danceability"] >= (mood/2)
#             and track_data["energy"] >= (mood/1.75)):
#         selected_tracks_uri.append(track_data["uri"])
# elif mood >= 0.90:
#     if ((mood - 0.15) <= track_data["valence"] <= 1
#         and track_data["danceability"] >= (mood/1.75)
#             and track_data["energy"] >= (mood/1.5)):
#         selected_tracks_uri.append(track_data["uri"])
#

# to find the emotion detected by words
