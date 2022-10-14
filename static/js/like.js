function like(postID, userID){
  let entry = {
    function : "like"
  }

  fetch(`${window.origin}/like/${postID}/${userID}`, {
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
      
      if(data["isliked"] === "already"){
        document.getElementById(`like-btn-${postID}`).innerHTML = 
        `<i class="bi bi-hand-thumbs-up" id="like-${postID}" style="color: dodgerblue; font-style: normal; font-size: medium;"> ${data["likes"]}</i>`
        
        document.getElementById(`like-count-${userID}-${postID}`).remove()
        if(data["likes"] == 0){
          document.getElementById(`like-list-${postID}`).innerHTML = 
          `<li  id = "null-${postID}"><a class="dropdown-item">No likes</a></li>`
        }
      }else{
        document.getElementById(`like-btn-${postID}`).innerHTML = 
        `<i class="bi bi-hand-thumbs-up-fill" id="like-${postID}" style="color: dodgerblue; font-style: normal; font-size: medium;"> ${data["likes"]}</i>`

        try{
          document.getElementById(`null-${postID}`).remove()
        }
        catch(err){}

        document.getElementById(`like-list-${postID}`).innerHTML += 
        `<li id = 'like-count-${userID}-${postID}'><a class="dropdown-item" href="/dashboard/${data['author_id']}" title=" ${data['date_created']} " ><img src="static/${data['author_img_path']}" style="width: 35px; clip-path: circle()"><b> ${data['author']} </b></a></li>`
      }
      

    })
  })
}