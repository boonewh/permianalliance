document.addEventListener("DOMContentLoaded", function () {
  const trailers1 = document.querySelector(".trailers1");
  const trailers2 = document.querySelector(".trailers2");
  const trailers3 = document.querySelector(".trailers3");

  const options = {
    root: null,
    rootMargin: "0px",
    threshold: 0.4,
  };

  const observer = new IntersectionObserver(function (entries, observer) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("appear");
        observer.unobserve(entry.target);

        // Delay the appearance of the next trailers
        if (entry.target === trailers1) {
          setTimeout(() => trailers2.classList.add("appear"), 1000);
          setTimeout(() => trailers3.classList.add("appear"), 2000);
        }
      }
    });
  }, options);

  observer.observe(trailers1);
});
