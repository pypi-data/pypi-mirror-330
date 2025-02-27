
from aiohttp import ClientSession
import asyncio,random,json
import aiofiles,random,aiohttp
from pathlib import Path
from tqdm import tqdm


class rubino:
	def __init__(self, auth):
		self.auth = auth
		print("rabino starts......")
		print("Creator : Mamadcoder \nid Telegram: https://t.me/RMSource")
	async def __aenter__(self):
		
		self.session = ClientSession()
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		if self.session:
			await self.session.close()
		return None

	async def GET(self, url):
		if not self.session:
			raise RuntimeError("Session is not initialized")
		async with self.session.get(url) as res:
		          data = await res.text()
		          return data
	
	async def POST_DATA(self, method:str,input:dict,auth=None) -> dict:
		
		url = f"https://rubino{random.randint(1,30)}.iranlms.ir/"
		async with self.session.post(url=url,json={"api_version": "0","auth": self.auth if not auth else auth,"client":{"app_name":"Main","app_version":"3.5.7","lang_code":"fa","package":"app.rbmain.a","temp_code":"31","platform":"Android"},"data": input,"method": method}) as res:
				data = await res.json()
				return data
	async def get_me(self,profile_id=None):
		return await self.POST_DATA("getMyProfileInfo",{ "profile_id": profile_id})
	async def follow(self,follow_id:str,profile_id:str=None) -> str:
		return await self.POST_DATA('requestFollow',{"f_type": "Follow","followee_id": follow_id,"profile_id": profile_id})
	async def post_byte(self,url,data,header):
		async with self.session.post(url=url,data=data,headers=header) as res:
			data = await res.json()
			
			return data
	
	async def upload_chunk(self, url, data, headers):
   	 async with self.session.post(url=url, data=data, headers=headers) as res:
      	  return await res.json()
	async def fetch_file_content(self,url):
		async with self.session.get(url) as response:
			if response.status == 200:
				content = await response.read()
				return content
			else:
				raise Exception(f"Failed to fetch file: {response.status}")
	async def upload_file(self, file, Type="Picture", profile_id=None, file_name=None):
	    
	    if not Path(file).exists():
	        bytef = await self.fetch_file_content(file)
	        if Type == "Picture":
	        	file_name = file_name if file_name else "rabino.jpg"
	        elif Type == "Video":
	        	file_name = file_name if file_name else "rabino.mp4"
	    else:
		    async with aiofiles.open(file, mode='rb') as f:
		        bytef = await f.read()
	
	    
	    REQUEST = {
	        "file_name": file_name if file_name else Path(file).name,
	        "file_size": len(bytef),
	        "file_type": Type,
	        "profile_id": profile_id
	    }
	    RESPONS = await self.POST_DATA("requestUploadFile", REQUEST)
	
	    file_id = RESPONS["data"]["file_id"]
	    hash_send = RESPONS["data"]["hash_file_request"]
	    url = RESPONS["data"]["server_url"]
	
	    headers = {
	        'auth': self.auth,
	        'Host': url.replace("https://", "").replace("/UploadFile.ashx", ""),
	        'chunk-size': str(len(bytef)),
	        'file-id': str(file_id),
	        'hash-file-request': hash_send,
	        "content-type": "application/octet-stream",
	        "accept-encoding": "gzip",
	        "user-agent": "okhttp/3.12.1"
	    }
	    chunk_size = 131072
	    chunks = [bytef[i:i + chunk_size] for i in range(0, len(bytef), chunk_size)]
	    progress_bar = tqdm(total=len(bytef), unit='B', unit_scale=True, desc="Uploading")
	    tasks = []
	    for i, chunk in enumerate(chunks, start=1):
	        headers['chunk-size'] = str(len(chunk))
	        headers['part-number'] = str(i)
	        headers['total-part'] = str(len(chunks))
	        
	        results = await self.upload_chunk(url, chunk, headers)
	        
	        progress_bar.update(len(chunk))
	      
	    progress_bar.close()
	    
	    return [RESPONS["data"], results['data']['hash_file_receive']]
	 
	async def add_post(self,file,text:str=None,type="Picture",profile_id=None,thumbnail=None,file_name=None):
		"""
		Type File Upload 
		# Picture 
		# Video
		"""
		data = await self.upload_file(file,Type=type,file_name=file_name,profile_id=profile_id)
		
		if type == "Picture":
			hashFile = data[1]
			fileID = data[0]["file_id"]
			thumbnailID = data[0]["file_id"]
			thumbnailHash = data[1]
			input = {"caption": text, "file_id": fileID, "hash_file_receive": hashFile, "height": 800, "width": 800, "is_multi_file": False, "post_type": "Picture", "rnd": random.randint(100000, 999999999), "thumbnail_file_id": thumbnailID, "thumbnail_hash_file_receive": thumbnailHash, "profile_id": profile_id}
			return await self.POST_DATA("addPost",input)
		elif type == "Video":
			hash = await self.upload_file("https://github.com/vs-mamad/rabino/raw/refs/heads/main/IMG_20250226_222517.png" if not thumbnail else thumbnail, Type="Picture",file_name="thumbnail.jpg",profile_id=profile_id)
			input = {"caption":text,"duration":"8","file_id":data[0]["file_id"],"hash_file_receive": data[1],"height":"1410","is_multi_file":None,"post_type":"Video","rnd":random.randint(100000, 999999999),"snapshot_file_id":hash[0]["file_id"],"snapshot_hash_file_receive":hash[1],"tagged_profiles":[],"thumbnail_file_id": hash[0]["file_id"],"thumbnail_hash_file_receive": hash[1],"width":"1080","profile_id":profile_id}
			
			return await self.POST_DATA("addPost",input)
	async def get_post_by_share_link(self,link:str,profile_id:str=None):
		if link.startswith("https://rubika.ir/post/"):
			link = link.split()[0][23:]
			input = {"share_string":link,"profile_id":profile_id}
		else:
			input = {"share_string":link,"profile_id":profile_id}
		return await self.POST_DATA("getPostByShareLink",input)
	async def add_post_view_count(self,post_id:str,target_post_id:str,profile_id=None) -> str:
		return await self.POST_DATA("addPostViewCount", {"post_id":post_id,"post_profile_id":target_post_id,"profile_id":profile_id})
	async def delete_post(self,post_id,profile_id=None):
		return await self.POST_DATA("removeRecord", {"model" : "Post","profile_id" : profile_id,"record_id" : post_id})
	async def get_explore_posts(self,limit=21,sort="FromMax",max_id=None,profile_id=None):
		return await self.POST_DATA("getExplorePosts", {"profile_id":profile_id,"limit":limit,"sort":sort,"max_id":max_id})
	async def search_profile(self,username,limit=20,profile_id=None):
		return await self.POST_DATA("searchProfile",{"username":username,"limit":limit,"profile_id":profile_id})
	async def search_hash_tag(self,content,limit=20,profile_id=None):
		return await self.POST_DATA("searchHashTag",{"content":content,"limit":limit,"profile_id":profile_id})
	async def un_follow(self,id,profile_id=None):
		return await self.POST_DATA("requestFollow",{"followee_id":id,"f_type":"Unfollow","profile_id":profile_id})
		
	
	async def get_profile_stories(self,limit:int=100,profile_id=None):
		return await self.POST_DATA("getProfileStories", {"limit": limit, "profile_id": profile_id})
		
	async def get_story_ids(self,target_profile_id,profile_id=None):
		return await self.POST_DATA("getStoryIds",{"profile_id":profile_id,"target_profile_id":target_profile_id})
	async def get_comments(self,post_id:str,post_profile_id:str,limit=100,profile_id=None,sort="FromMax",equal=False):
		return await self.POST_DATA("getComments",{"equal": equal, "limit": limit, "sort": sort, "post_id": post_id, "profile_id": profile_id, "post_profile_id": post_profile_id})
	async def get_profile_list(self,equal=False,limit=10,sort="FromMax"):
		return await self.POST_DATA("getProfileList",{"equal":equal,"limit":limit,"sort":sort})
		
	async def get_my_profile_info(self,profile_id=None):
		return await self.POST_DATA("getMyProfileInfo",{"profile_id":profile_id})
		
	async def like_post(self,post_id:str,target_post_id:str,profile_id=None):
		return await self.POST_DATA("likePostAction",{"action_type":"Like","post_id":post_id,"post_profile_id":target_post_id,"profile_id":profile_id})
	async def get_share_link(self,post_id,post_profile_id,profile_id=None):
		return await self.POST_DATA("getShareLink",{"post_id":post_id,"post_profile_id":post_profile_id,"profile_id":profile_id})
	async def search_username(self,username:str)-> str:
		if username.startswith("@"):
			input = {"username": username.replace("@","")}
		else:
			input = {"username": username}
		return await self.POST_DATA("isExistUsername",input)
		
	async def add_view_story(self,story_profile_id:str,story_ids:list,profile_id=None):
		return await self.POST_DATA("addViewStory",{"profile_id":profile_id,"story_ids":story_ids,"story_profile_id":story_profile_id})
	async def create_page(self,name,username,bio=None):
		return await self.POST_DATA("createPage",{"bio": bio,"name": name,"username": username})
	async def add_comment(self,text,post_id,post_profile_id,profile_id=None):
		return await self.POST_DATA("addComment",{"content": text,"post_id": post_id,"post_profile_id": post_profile_id,"rnd":f"{random.randint(000000,999999)}" ,"profile_id":profile_id})
	async def get_profile_posts(self,target_profile_id,limit=1,profile_id=None):
		return await self.POST_DATA("getProfilePosts",{"limit":limit,"sort":"FromMax","target_profile_id":target_profile_id,"profile_id":profile_id})
	async def un_like_post(self,post_id,post_profile_id,profile_id=None):
		return await self.POST_DATA("likePostAction", {"action_type":"Unlike","post_id":post_id,"post_profile_id":post_profile_id,"profile_id":profile_id})
	async def post_book_mark_action(self,post_id,post_profile_id,profile_id=None):
		return await self.POST_DATA("postBookmarkAction",{"action_type":"Bookmark","post_id":post_id,"post_profile_id":post_profile_id,"profile_id":profile_id})
