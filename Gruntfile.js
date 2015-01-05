module.exports =  function(grunt){
  require('load-grunt-tasks')(grunt);

  grunt.initConfig({
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
