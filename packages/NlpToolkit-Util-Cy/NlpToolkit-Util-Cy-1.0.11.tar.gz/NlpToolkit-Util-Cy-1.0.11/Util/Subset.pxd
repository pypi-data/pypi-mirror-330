cdef class Subset(object):
        cdef list set
        cdef int __rangeEnd, element_count

        cpdef list get(self)
        cpdef bint next(self)
