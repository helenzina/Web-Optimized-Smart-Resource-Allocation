const semesters = document.querySelector('.semesters');
const courses = document.querySelector('.courses');
const labs = document.querySelector('.labs');
const preview = document.querySelector('.preview');
const buttons = document.querySelector('.buttons');
const form = document.querySelector('form');

// TODO: the function will check first: if the selected semester is in (1,7), show labs
// else show elective courses for 8 & 9

// This function ensures the semesters will be selected one at a time
// and displays the courses as well depending on the selected semester
document.querySelectorAll('.semester-item').forEach(item => {
    item.addEventListener('click', function () {
        item.classList.add('active');
        const activeItem = item;

        document.querySelectorAll('.semester-item').forEach(otherItem => {
            if (otherItem !== activeItem) {
                otherItem.classList.remove('active');
            }
        });

        semesters.addEventListener('click', function () {
            semesters.style.display = 'inline-flex';
            form.classList.add('content');
        });

        courses.classList.remove('hidden');
        courses.style.opacity = 1;
        courses.style.transform = 'translateX(0)';

        labs.classList.add('hidden');
    });
});

// This function ensures the courses will be selected one at a time
// and displays the labs as well depending on the selected course
document.querySelectorAll('.course-item').forEach(item => {
    item.addEventListener('click', function () {
        item.classList.add('active');
        const activeItem = item;

        document.querySelectorAll('.course-item').forEach(otherItem => {
            if (otherItem !== activeItem) {
                otherItem.classList.remove('active');
            }
        });

        courses.classList.remove('hidden');
        courses.style.opacity = 1;
        courses.style.transform = 'translateX(0)';

        labs.classList.add('hidden');
    });
});

document.querySelectorAll('.course-item').forEach(item => {
    item.addEventListener('click', function () {
        labs.classList.remove('hidden');
        labs.style.opacity = 1;
        labs.style.transform = 'translateX(0)';

        //TODO: preview will stay hidden until a lab is selected
        preview.classList.remove('hidden');
        preview.style.opacity = 1;
        preview.style.transform = 'translateX(0)';
    
        buttons.style.display = 'inline-flex';
        buttons.style.alignContent ='flex-end';
    });
});

//TODO: if an option is selected in labs, gets deleted and cannot be selected again by another lab


const saveButton = document.querySelector('button[type="submit"]');
const resetButton = document.querySelector('button[type="reset"]');

//TODO: save button submits the selected labs to database,
//e.g. INSERT INTO programming1_lab1 VALUES ('John', 'Doe', 12345, 1) ...

//TODO: reset button clears the selected labs and the preview table
