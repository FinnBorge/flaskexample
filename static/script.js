/*
 * //.detach().get();

var sortForks = $('#sort-forks');
var sortStars = $('#sort-stars');
var sortContributors = $('#sort-contributors');

function sortRepos(sortValue) {
  var repoList, repos, i, inProgress, shouldMove;
  inProgress = true;
  while (inProgress) {
    inProgress = false;
    repoList = $('#repo-list');
    repos = repoList.children('.repository')
    for (i = 0; i < (repos.length - 1); i++) {
      shouldMove = false;
      if (repos[i].dataset[sortValue] > repos[i + 1].dataset[sortValue]) {
        shouldMove = true;
        break;
      }
    }
    if (shouldMove) {
      repos[i].parentNode.insertBefore(repos[i + 1], repos[i]);
      inProgress = true;
    }
  }
}
*/


function sortForks() {
  $("#repo-list li.repository").sort(sort_li)
                    .appendTo('#repo-list');
  function sort_li(a, b) {
    return ($(b).data('forkCount')) < ($(a).data('forkCount')) ? 1 : -1;
  }
};

function sortStars() {
  $("#repo-list li.repository").sort(sort_li)
                    .appendTo('#repo-list');
  function sort_li(a, b) {
    return ($(b).data('starCount')) < ($(a).data('starCount')) ? 1 : -1;
  }
};

function sortContributors() {
  $("#repo-list li.repository").sort(sort_li)
                    .appendTo('#repo-list');
  function sort_li(a, b) {
    return ($(b).data('contributorCount')) < ($(a).data('contributorCount')) ? 1 : -1;
  }
};

$(function() {
  $('#sort-forks').click(sortForks());
  $('#sort-stars').click(sortStars());
  $('#sort-contributors').click(sortContributors());
});
