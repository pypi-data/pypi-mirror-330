#ifndef CPL_CONFIG_H
#define CPL_CONFIG_H
/* We define this here in general so that a VC++ build will publicly
   declare STDCALL interfaces even if an application is built against it
   using MinGW */

#ifndef CPL_DISABLE_STDCALL
#  define CPL_STDCALL __stdcall
#endif

/* Define if you don't have vprintf but do have _doprnt.  */
#undef HAVE_DOPRNT

/* Define if you have the vprintf function.  */
#ifndef HAVE_VPRINTF
  #define HAVE_VPRINTF 1
#endif
#ifndef HAVE_VSNPRINTF
  #define HAVE_VSNPRINTF 1
#endif
#ifndef HAVE_SNPRINTF
  #define HAVE_SNPRINTF 1
#endif

#define HAVE_GETCWD 1
/* gmt_notunix.h from GMT project also redefines getcwd. See #3138 */
#ifndef getcwd
#define getcwd _getcwd
#endif

/* Define if you have the ANSI C header files.  */
#ifndef STDC_HEADERS
#  define STDC_HEADERS 1
#endif

/* Define to 1 if you have the <assert.h> header file. */
#define HAVE_ASSERT_H 1

/* Define to 1 if you have the <fcntl.h> header file.  */
#define HAVE_FCNTL_H 1

/* Define if you have the <unistd.h> header file.  */
#undef HAVE_UNISTD_H

/* Define if you have the <stdint.h> header file.  */
#undef HAVE_STDINT_H

/* Define to 1 if you have the <sys/types.h> header file. */
#define HAVE_SYS_TYPES_H 1

#undef HAVE_LIBDL

/* Define to 1 if you have the <locale.h> header file. */
#define HAVE_LOCALE_H 1

#define HAVE_FLOAT_H 1

#define HAVE_ERRNO_H 1

#define HAVE_SEARCH_H 1

/* Define to 1 if you have the <direct.h> header file. */
#ifndef HAVE_DIRECT_H
  #define HAVE_DIRECT_H 1
#endif

/* Define to 1 if you have the `localtime_r' function. */
#undef HAVE_LOCALTIME_R

#undef HAVE_DLFCN_H
#undef HAVE_DBMALLOC_H
#undef HAVE_LIBDBMALLOC
#undef WORDS_BIGENDIAN

/* The size of a `int', as computed by sizeof. */
#define SIZEOF_INT 4

/* The size of a `long', as computed by sizeof. */
#define SIZEOF_LONG 4

/* The size of a `unsigned long', as computed by sizeof. */
#define SIZEOF_UNSIGNED_LONG 4

/* The size of `void*', as computed by sizeof. */
#ifdef _WIN64
# define SIZEOF_VOIDP 8
#else
# define SIZEOF_VOIDP 4
#endif

/* Define as 0 or 1 according to the floating point format supported by the
   machine */
#define HAVE_IEEEFP 1

/* Define to `__inline__' or `__inline' if that's what the C compiler
   calls it, or to nothing if 'inline' is not supported under any name.  */
#ifndef __cplusplus
#  ifndef inline
#    define inline __inline
#  endif
#endif

#define lfind _lfind

#define VSI_STAT64 _stat64
#define VSI_STAT64_T __stat64

#pragma warning(disable: 4786)

/* Define to 1, if your compiler supports long long data type */
#define HAVE_LONG_LONG 1
#endif /* CPL_CONFIG_H */
