document.querySelectorAll('.semester-item').forEach(item => {
    item.addEventListener('click', function () {
        item.classList.add('active');
        const activeItem = item;

        document.querySelectorAll('.semester-item').forEach(otherItem => {
            if (otherItem !== activeItem) {
                otherItem.classList.remove('active');
            }
        });

        document.querySelector('.courses').classList.remove('hidden');
        document.querySelector('.courses').style.opacity = 1;
        document.querySelector('.courses').style.transform = 'translateX(0)';

        document.querySelector('.labs').classList.add('hidden');
    });
});

document.querySelectorAll('.course-item').forEach(item => {
    item.addEventListener('click', function () {
        item.classList.add('active');
        const activeItem = item;

        document.querySelectorAll('.course-item').forEach(otherItem => {
            if (otherItem !== activeItem) {
                otherItem.classList.remove('active');
            }
        });

        document.querySelector('.courses').classList.remove('hidden');
        document.querySelector('.courses').style.opacity = 1;
        document.querySelector('.courses').style.transform = 'translateX(0)';

        document.querySelector('.labs').classList.add('hidden');
    });
});

document.querySelectorAll('.course-item').forEach(item => {
    item.addEventListener('click', function () {
        document.querySelector('.labs').classList.remove('hidden');
        document.querySelector('.labs').style.opacity = 1;
        document.querySelector('.labs').style.transform = 'translateX(0)';

        document.querySelector('.preview').classList.remove('hidden');
        document.querySelector('.preview').style.opacity = 1;
        document.querySelector('.preview').style.transform = 'translateX(0)';
    
        document.querySelector('.buttons').style.display = 'flex';
    });
});
