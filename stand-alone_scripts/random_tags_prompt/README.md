## random_tags_prompt.py

Generates a prompt of random danbooru tags (names and sources mostly excluded)

Usage:   
`python random_tags_prompt.py` - you need to clarify a number of tags in the file   
or    
`python random_tags_prompt.py NUMBER_OF_TAGS`      

You can get tags in [this repository](https://github.com/DominikDoom/a1111-sd-webui-tagcomplete/tree/main/tags) or use the copy in here (possibly outdated)


## random_tags_booru.py

Generates a prompt of random danbooru or gelbooru posts (by default it uses only general tags, it could be changed inside)    

Usage :  
`python random_tags_booru.py` - fetched tags from the SOURCE variable site   
`python random_tags_booru.py BOORU`  -  fetched tags from the explicitly stated site (supports danbooru, gelbooru, safebooru, e926, and e621)   


You also can fetch tags from a specific post from the booru site:   
`python random_tags_booru.py url "URL"`

Experimental feature for `safebooru`:   
`python random_tags_booru.py search safebooru TAG-OR-SOMETHING`


## for_dataset.py

Downloads an image and create a txt file with all the tags.    

Usage:  # Only from gelbooru, danbooru, safebooru, e621, and e926  
`python for_dataset.py "url-of-an-image"`    
`python for_dataset.py txt "txt-file-with-urls.txt"` 
