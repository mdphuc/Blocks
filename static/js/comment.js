function comment(postID){
    cmt = document.getElementById(`comment-${postID}`)
    


  let entry = {
    text : cmt.value,

  }

  fetch(`${window.origin}/create_comment/${postID}`, {
    method: 'POST',
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "content-type" : "application/json"
    })
  }).then(function(response){
    if (response.status !== 200){
      console.log(`Failed : ${response.status}`)
      return
    }

    response.json().then(function(data){
      
      document.getElementById(`commentl-${postID}`).innerHTML += 
      `
      <div class="card-text d-flex " style="color: black">
        <div class="dropdown">
          <button class="button1 dropdown-toggle" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
            <i class="bi bi-caret-down-fill" style="font-size: small;"></i>
          </button>				
          <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">  
            <form method="POST" action="/delete_comment/${data["post_id"]}/${data["id"]}" id = "delete-comment-${data["post_id"]}-${data["id"]}">
              <li><button class="dropdown-item" type="submit">Delete</button></li> 
            </form>	
            
            <li><a data-bs-toggle="collapse" href="#edit-comment-${data["post_id"]}-${data["id"]}" style="text-decoration: none;" class="dropdown-item">Edit</a></li> 

          </ul>

        </div>
        <p title="${data["date_created"]}"><a  href="/dashboard/${data["author_id"]}" style="color: black;font-size: large; text-decoration: none;"><img src="/static/${data["author_img_path"]}" style="width: 35px; clip-path: circle()"><b> ${data["author"]} </b></a>: ${data["text"]}</p>
      </div>
      <div id = "edit-comment-${data["post_id"]}-${data["id"]}" class="collapse">
        <div class="card-text d-flex " style="color: black">
          <a class="btn-close" data-bs-toggle="collapse" href="#edit-comment-${data["post_id"]}-${data["comment_id"]}" style="text-decoration: none; font-size: x-small;" role="button" href=""></a>
          <input type="text" placeholder="Edit..." name="edited_comment" id = "comment-edited-${data["post_id"]}-${data["comment_id"]}" style="width: 95%; border-radius: 16px; border: 1px solid rgb(0, 0, 0, 0.1) ; background-color: transparent; text-indent: 15px;">
          <button type="submit" style="border: transparent; background-color: transparent;" id="submit" value = '${data["post_id"]}' title="Comment" ><i class="bi bi-box-arrow-up" style="color: black;" title="Update" onclick="like_change()"></i></button>
        </div> 
      </div>
        
        `
      document.getElementById(`comment-${postID}`).value = ""
      
      

    })
  })

}