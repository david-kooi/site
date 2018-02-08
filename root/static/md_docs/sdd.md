# Cbuf16 Circular Buffer 

## 1. Introduction
### Standard Implementation
The Cbuf16 is a fixed width 16 bit FIFO circular buffer.
Values are added to the HEAD of the buffer and removed from the TAIL.
If the CBUF16\_SIZE is reached the oldest value(The value at the TAIL) is removed.

### Fixed Margin Implementation
A fixed margin implementation is also included. This implementation
allows values to be collected before and after a trigger. 
The buffer fills to half of the MEMORY_DEPTH and circulates with that size. 
Upon a trigger condition the buffer fills up the next half of MEMORY_DEPTH. 


## 2. Standard Usage 
A Cbuf16 struct is defined in Cbuf16.h. The Cbuf16 struct is
initialized by `Cbuf16Init(Cbuf16 *buf_t)`.

- Values are added to the HEAD of the buffer by using `PutCbuf16(Cbuf16 *buf_t, uint16_t val)`.
- Values are removed from the TAIL of the buffer by using `GetCbuf16(Cbuf16_t). I.e the tail 
pointer increases when `GetCbuf16` is called. 

## 3. Standard Structures and Functions
###3.1 Cbuf16 Struct
```C
 typedef struct{
	uint32_t head,tail; // Head and tail pointers
	uint32_t size;      // Size of U16 array
	uint16_t *buf;      // U16 array

	uint8_t FIRST; // Flag indicating an initial state

 }Cbuf16;

A Cbuf16 can be initialized with a maximum of size of 32 bits. (4294967296) 

```

### 3.2 Cbuf16 Functions
Return Value | Function| | Arguments | Description |  
----------- | ----------- | -------------------
void | InitCbuf16 | Cbuf16 *buf_t, uint32_t size | Allocates an array of size CBUF16_SIZE for a Cbuf16 structure. Initializes head and tail pointers to 0. 
void FreeCbuf16 | Cbuf16 *buf_t | Frees the Cbuf16's array. Does not free the structure.
int16_t | PutCbuf16 | Cbuf16 *buf_t, uint16_t val | Adds val to the head of the Cbuf16. Returns the index of the inserted value.
iunt32_t | GetCbuf16 | Cbuf16 *buf_t | Removes and returns a value from the tail. The tail pointer is incremented during usage. Returns -1 if the Cbuf16 is exahusted. (# gets == # puts) 




## 4. Windowed Usage


