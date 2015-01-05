module.exports =  function(grunt){
  require('load-grunt-tasks')(grunt);

  grunt.initConfig({
    watch:{
      options:{livereload: true},
      sass:{
        files: ['static/sass/*.scss'],
        tasks: ['sass'],
      }
    },
    sass:{
      dist:{
        files:{
          'static/css/style.css': 'static/sass/style.scss',
        }
      }
    }
  })
  //grunt.registerTask('sass', [])
};
