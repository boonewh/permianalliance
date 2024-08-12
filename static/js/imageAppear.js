document.addEventListener("DOMContentLoaded", function () {
  const images = document.querySelectorAll(".about img, #features img");

  const options = {
    root: null,
    rootMargin: "0px",
    threshold: 0.5,
  };

  const observer = new IntersectionObserver(function (entries, observer) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("appear");
        observer.unobserve(entry.target); // Stop observing after it has appeared
      }
    });
  }, options);

  images.forEach((image) => {
    observer.observe(image);
  });
});
