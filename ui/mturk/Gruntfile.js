/*global module:false*/
module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    // Metadata.
    timestamp: new Date().getTime(),
    pkg: grunt.file.readJSON('package.json'),
    banner: '/*! <%= pkg.title || pkg.name %> - v<%= pkg.version %> - ' +
      '<%= grunt.template.today("yyyy-mm-dd") %>\n' +
      '<%= pkg.homepage ? "* " + pkg.homepage + "\\n" : "" %>' +
      '* Copyright (c) <%= grunt.template.today("yyyy") %> <%= pkg.author.name %>;' +
      ' Licensed <%= _.pluck(pkg.licenses, "type").join(", ") %> */\n',
    // Task configuration.
    clean: {
      dist: ["dist"]
    },

    concat: {
      'mturkjs': {
        src: [
	  "vendor/js/angular.js",
	  "vendor/js/angular-resource.js",
	  "vendor/js/lodash.js",
	  "vendor/js/xeditable.js",
	  "js/app.js"
	],
        dest: 'dist/mturk.js'
      },
      'mturkcss': {
        src: [
	  "vendor/css/bootstrap.min.css",
	  "css/style.css"
	],
        dest: 'dist/mturk.css'
      }
    },

    uglify: {
      'mturkjs': {
        src: 'dist/mturk.js',
        dest: 'dist/mturk.<%= timestamp %>.min.js'
      }
    },

    cssmin: {
      options: {
        compatibility: 'ie8',
        keepSpecialComments: '*'
      },
      'mturkcss': {
        files: {
          'dist/mturk.<%= timestamp %>.min.css': 'dist/mturk.css',
        }
      }
    },

    copy: {
      options: {},
      fonts: {
        expand: true,
        src: 'vendor/fonts/*',
        dest: 'dist/fonts/',
	filter: 'isFile',
	flatten: true
      },
      images: {
        expand: true,
        src: 'img/*',
        dest: 'dist/img/',
	filter: 'isFile',
	flatten: true
      },
      'index-test': {
        src: 'index.html',
	dest: 'dist/test/index.html'
      },
      'test-test': {
        src: 'test.html',
	dest: 'dist/test/test.html'
      },
      'fonts-test': {
        expand: true,
        src: 'vendor/fonts/*',
        dest: 'dist/test/fonts/',
	filter: 'isFile',
	flatten: true
      },
      'images-test': {
        expand: true,
        src: 'img/*',
        dest: 'dist/test/img/',
	filter: 'isFile',
	flatten: true
      },
      'css-test': {
        src: 'dist/mturk.css',
        dest: 'dist/test/mturk.css',
      }
    },
    'string-replace': {
      index: {
        files: {
          'dist/index.html': 'index.html',
        },
        options: {
          replacements: [
            {
              pattern: '<script src="mturk.js"></script>',
              replacement: '<script src="mturk.<%= timestamp %>.min.js"></script>'
            },
            {
              pattern: 'href="mturk.css"',
              replacement: 'href="mturk.<%= timestamp %>.min.css"'
            },
          ]
        }
      },
      'js-test': {
        files: {
          'dist/test/mturk.js': 'dist/mturk.js',
        },
        options: {
          replacements: [
            {
              pattern: '//check if referrer ends with mturk.com',
              replacement: 'return true;'
            }
          ]
        }
      }

    }
  });

  // These plugins provide necessary tasks.
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-string-replace');

  // Default task.
  grunt.registerTask('default', ['clean', 'concat', 'uglify', 'cssmin', 'copy', 'string-replace']);

};

