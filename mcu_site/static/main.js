const reviewform = document.getElementById('review-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

reviewform.addEventListener('submit', function(event){
    console.log("Review Submitted");
    event.preventDefault();
    submitreviewform();
}, false);

function submitreviewform(){    
    const movieoptionsbox = document.getElementById('title')
    var selectedmov = movieoptionsbox.options[movieoptionsbox.selectedIndex].value
    var numstars = document.getElementById('stars').value
    var revtext = document.getElementById('review_text').value
    var authorid = document.getElementById('author').value

    $.ajax({
        url: "/submit-review/",
        type: "POST",
        data: {title:selectedmov, stars:numstars, review_text:revtext, author:authorid, csrfmiddlewaretoken: window.CSRF_TOKEN},

        success:function(){
            console.log("SUCCESS!")
            $('#statusmsg').html("Your review was successfully received!")
        },
        error:function(error){
            console.log("ERROR")
            $('#statusmsg').html(error.responseJSON.error)
        },
    });
};

/*const sortbyform = document.getElementById('sortbyform')
const sortbyselectionbox = document.getElementById('sortoptions')
const movlist = document.getElementById('movieslist')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

console.log(csrf)

sortbyform.addEventListener('submit', function(event){
    console.log("Sort Selected!");
    event.preventDefault();
    console.log(sortbyselectionbox);
    display_sort();
}, false);

function display_sort(){
    var strsortby = sortbyselectionbox.options[sortbyselectionbox.selectedIndex].value
    console.log(strsortby)
    $.ajax({
        url: "/movies/",
        type: "POST",
        data: {sortby:strsortby, csrfmiddlewaretoken: window.CSRF_TOKEN},

        success:function(json){
            console.log(json)
        }
    });
};

console.log(sortbyform)*/