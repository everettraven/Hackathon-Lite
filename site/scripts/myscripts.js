var auth_token = "";

function register()
{
    var formData = JSON.stringify($('#register form').serializeArray());
    var jsonData = {};
    formData = JSON.parse(formData);

    jsonData["username"] = formData[0]["value"];
    jsonData["password"] = formData[1]["value"];
    jsonData["access_token"] = formData[2]["value"];

    console.log(jsonData);

    $.ajax(
        {
            type: "POST",
            url: "http://localhost:5000/user/register",
            data: JSON.stringify(jsonData),
            dataType: "json",
            contentType: "application/json"
        }
    );

}

function logIn()
{

    var formData = JSON.stringify($('#login form').serializeArray());
    var jsonData = {};
    formData = JSON.parse(formData);

    console.log(formData);

    jsonData["username"] = formData[0]["value"];
    jsonData["password"] = formData[1]["value"];

    console.log(jsonData);

    $.ajax(
        {
            type: "POST",
            url: "http://localhost:5000/user/login",
            data: JSON.stringify(jsonData),
            success: function (result) {
                auth_token = result.access_token;
                console.log(auth_token);
                sessionStorage.setItem("auth_token", auth_token)
                window.location.href = "homepage.html";
            },
            dataType: "json",
            contentType: "application/json"
        }
    )

}



function getData()
{

    var ul = $('#basics');

    $.ajax(
        {
            type: "GET",
            beforeSend: function (request) {
                request.setRequestHeader("Authorization", "Bearer " + sessionStorage.getItem("auth_token"));
            },
            url: "http://localhost:5000/user/data",
            success: function (result) {

                console.log(result);

                for(var i = 0; i < result.length; i++)
                {
                    var courseName = result[i]["course_name"];
                    ul.append("<li class='cd-faq__title'><h2>"+ courseName +"</h2></li>")
                    if(result[i]["assignments"].length > 0)
                    {
                        for(var j = 0; j < result[i]["assignments"].length; j++)
                        {
                            var assignmentName = result[i]["assignments"][j]["name"];
                            var assignmentDescrip = result[i]["assignments"][j]["description"];
                            var assignmentDueAt = result[i]["assignments"][j]["due_at"];

                            ul.append("<li class='cd-faq__item'><a class='cd-faq__trigger' href='#0'><span>"+ assignmentName +"</span></a><div class='cd-faq__content'><div class='text-component'><p>Due:"+ assignmentDueAt +"</p>"+ assignmentDescrip +"</div></div></li>");
                        }
                    }
                    else{
                        ul.append("<li class='cd-faq__item'><a class='cd-faq__trigger' href='#0'><span>Nothing to do!</span></a><div class='cd-faq__content'><div class='text-component'><p>Due: N/A </p><p>There is nothing due for this class ya silly goose!</p></div></div></li>");

                    }
                }
            },
            fail: function(result) {
                console.log(result);
            },
            dataType: "json",
            contentType: "application/json"
        }
    )

}


/*

<li class="cd-faq__title"><h2>Programming Languages</h2></li>
			<li class="cd-faq__item">
				<a class="cd-faq__trigger" href="#0"><span>Assignment 1</span></a>
				<div class="cd-faq__content">
          			<div class="text-component">
						<p>Due: 9/01/2019</p>
						<p>For this homework, use Internet search engines to gather information on :

								U.S. Code, Title 18, Sec. 1030, which covers fraud and related activity in connections with computers. 
								OR 
								Federal Information Security Management Act - FISMA</p>
          			</div>
				</div> <!-- cd-faq__content -->
			</li>
*/