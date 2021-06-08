/**
 * Array with a set amount of available items.
 */
export default class LimitedList extends Array {

    constructor(maxSize) {
        super();

        this.maxSize = maxSize;
    }

    push(...items) {

        super.push(items);
        while(this.length > this.maxSize) {
           this.shift();
        }

        return this.length;
    }

}
