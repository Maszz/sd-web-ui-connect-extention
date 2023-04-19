var images_history_click_image = function (bnt, i) {
  // console.log("in images_history_click_image !" + i);
  var buttons = images_history_get_parent_by_tagname(
    bnt,
    "DIV"
  ).querySelectorAll(".thumbnail-item");
  var index = -1;
  var i = 0;
  buttons.forEach(function (e) {
    if (e == bnt) {
      index = i;
    }
    i++;
  });
  var gallery = images_history_get_parent_by_class(
    bnt,
    "_connect_browser_cantainor"
  );
  var set_btn = gallery.querySelector(".connect_browser_set_index");
  var curr_idx = set_btn.getAttribute("img_index", index);
  if (curr_idx != index) {
    set_btn.setAttribute("img_index", index);
  }
  set_btn.click();
};

function images_history_get_parent_by_class(item, class_name) {
  var parent = item.parentElement;
  while (!parent.classList.contains(class_name)) {
    parent = parent.parentElement;
  }
  return parent;
}

function images_history_get_parent_by_tagname(item, tagname) {
  var parent = item.parentElement;
  tagname = tagname.toUpperCase();
  while (parent.tagName != tagname) {
    parent = parent.parentElement;
  }
  return parent;
}

function images_history_get_current_img(tabname, page_index, state) {
  return [
    gradioApp()
      .getElementById(tabname + "_connect_browser_set_index")
      .getAttribute("img_index"),
    -state,
  ];
}

function images_history_init() {
  var tabnames = gradioApp().getElementById("connect_browser_tabnames_list");
  if (tabnames) {
    images_history_tab_list = tabnames
      .querySelector("textarea")
      .value.split(",");
    for (var i in images_history_tab_list) {
      var tab = images_history_tab_list[i];
      gradioApp()
        .getElementById(tab + "_connect_images_browser")
        .classList.add("_connect_browser_cantainor");
      gradioApp()
        .getElementById(tab + "_connect_browser_set_index")
        .classList.add("connect_browser_set_index");
      gradioApp()
        .getElementById(tab + "_images_history_del_button")
        .classList.add("images_browser_del_button");
      gradioApp()
        .getElementById(tab + "_connect_image_gallery")
        .classList.add("connect_browser_gallery");
    }
  }
}
let timer;
var images_history_tab_list = "";
setTimeout(images_history_init, 500);
document.addEventListener("DOMContentLoaded", function () {
  var mutationObserver = new MutationObserver(function (m) {
    if (images_history_tab_list != "") {
      for (var i in images_history_tab_list) {
        let tabname = images_history_tab_list[i];
        var buttons = gradioApp().querySelectorAll(
          "#" + tabname + "_connect_images_browser .thumbnail-item"
        );
        buttons.forEach(function (bnt, index) {
          bnt.addEventListener(
            "click",
            () => images_history_click_image(bnt, index),
            false
          );
        });
      }
    }
  });
  mutationObserver.observe(gradioApp(), { childList: true, subtree: true });
});
