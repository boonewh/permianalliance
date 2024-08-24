document.addEventListener("DOMContentLoaded", function () {
  const trailers1 = document.querySelectorAll(".trailers1");
  const trailers2 = document.querySelectorAll(".trailers2");
  const trailers3 = document.querySelectorAll(".trailers3");

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

        // Find index of the intersecting element to delay subsequent ones accordingly
        const index = [...trailers1].indexOf(entry.target);
        if (index !== -1) {
          setTimeout(() => trailers2[index].classList.add("appear"), 1000);
          setTimeout(() => trailers3[index].classList.add("appear"), 2000);
        }
      }
    });
  }, options);

  trailers1.forEach((trailer) => observer.observe(trailer));
});
