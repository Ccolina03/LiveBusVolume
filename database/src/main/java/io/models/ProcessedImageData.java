

static class ProcessedImageData {
    public long timestamp;
    public int id;
    public int count;

    public Event(long timestamp, int id, int count) {
        this.timestamp = timestamp;
        this.id = id;
        this.count = count;
    }
}