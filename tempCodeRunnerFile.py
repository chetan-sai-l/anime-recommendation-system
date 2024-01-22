data = []
    if k==1:
        for i in similar_items:
          item = []
        #   id = anime_url.loc[anime_url['name'] == pt.index[i[0]], 'anime_id'].values
        #   temp_df = anime_url_id[id]
          #temp_df = anime_url_id[anime_url['name'] == pt.index[i[0]]]
          if i[0]< len(pt1):
              tem_df = anime_url[anime_url['name'] == pt1.index[i[0]]]
          else:
              tem_df = anime_url[anime_url['name'] == pt2.index[i[0]-len(pt1)]]
          anime_id = tem_df['anime_id'].values[0]  # Assuming there's only one match, extract the anime_id
          temp_df = anime_url_id[anime_url_id['anime_id'] == anime_id]
          item.extend(list(tem_df['name'].values))
          item.extend(list(temp_df['main_picture'].values))
          item.extend(list(temp_df['url'].values))
          data.append(item)
    else:
        for i in similar_items:
          item = []
        #   id = anime_url.loc[anime_url['name'] == pt.index[i[0]], 'anime_id'].values
        #   temp_df = anime_url_id[id]
          #temp_df = anime_url_id[anime_url['name'] == pt.index[i[0]]]
          if i[0] < len(pt1):
              tem_df = anime_url[anime_url['name'] == pt1.index[i[0]]]
          else:
              tem_df = anime_url[anime_url['name'] == pt2.index[i[0]-len(pt1)]]
          anime_id = tem_df['anime_id'].values[0]  # Assuming there's only one match, extract the anime_id
          temp_df = anime_url_id[anime_url_id['anime_id'] == anime_id]
          item.extend(list(tem_df['name'].values))
          item.extend(list(temp_df['main_picture'].values))
          item.extend(list(temp_df['url'].values))
          data.append(item)