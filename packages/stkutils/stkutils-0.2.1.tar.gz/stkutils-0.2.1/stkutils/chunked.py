# package stkutils::chunked;
# use strict;
# use stkutils::debug qw(fail);
# use IO::File;
from pathlib import Path

from stkutils.binary_data import pack, unpack

MAYBE_CHUNK_LENGTH = 8


class chunked:
    def __init__(
        self,
        filename: str | None = None,
        mode: str | None = None,
        data: bytes | None = None,
    ):
        self.mode = mode
        if self.mode == "r":
            with open(filename, "rb") as fh:
                self.input_data = fh.read()

        elif self.mode == "w":
            if not Path(filename).parent.exists():
                Path(filename).parent.mkdir(parents=True)
            fh = open(filename, "bw")
            self.fh = fh
        elif self.mode == "data":
            self.input_data = data
        else:
            raise ValueError("wrong or missing mode")

        self.output_data = ""
        self.offset = 0
        self.glob_pos = []
        self.end_offsets = []
        self.start_offsets = []

    def close(self) -> None:
        if self.mode == "w":
            self.fh.close()
            self.fh = None
        else:
            self.input_data = None

    def r_chunk_open(self) -> tuple[int | None, int | None]:
        # my $self = shift;
        # offset = $self->{end_offsets}[$#{$self->{end_offsets}}];
        offset = self.end_offsets[-1] if self.end_offsets else None
        if offset is not None and self.offset >= offset:
            return None, None

        # defined($offset) && $self->{offset} >= $offset && return undef;
        if self.offset + MAYBE_CHUNK_LENGTH >= len(self.input_data):
            return None, None
        # return undef if length(${$self->{input_data}}) <= $self->{offset} + 8;
        data = self.input_data[self.offset : self.offset + MAYBE_CHUNK_LENGTH]
        # my $data = substr(${$self->{input_data}}, $self->{offset}, 8);
        # my ($index, $size) = unpack('VV', $data);
        (index, size) = unpack("VV", data)
        self.offset += MAYBE_CHUNK_LENGTH
        # $self->{offset} += 8;
        # push @{$self->{start_offsets}}, $self->{offset};
        # push @{$self->{end_offsets}}, ($self->{offset} + $size);
        self.start_offsets.append(self.offset)
        self.end_offsets.append(self.offset + size)
        return (index, size)

    def r_chunk_close(self) -> None:
        # my $self = shift;
        # my $offset = pop @{$self->{end_offsets}};
        offset = self.end_offsets.pop()
        if offset < self.offset:
            raise ValueError(
                f"current position ({self.offset}) is outside current chunk ({offset})",
            )
        # $self->{offset} <= $offset or fail('current position ('.$self->{offset}.') is outside current chunk ('.$offset.')');
        self.offset = max(self.offset, offset)

        # pop @{$self->{start_offsets}};
        self.start_offsets.pop()

    # }
    def find_chunk(self, chunk: int) -> int | None:
        # my $self = shift;
        # my ($chunk) = @_;
        gl_pos = self.offset
        offset = (
            self.end_offsets[-1] if self.end_offsets else None
        )  # self.end_offsets}[$#{$self->{end_offsets}}];
        if self.mode == "data" or self.mode == "r":
            if offset is None:
                offset = len(self.input_data)
        else:
            raise ValueError("cannot read data while in write-mode")

        # defined ($offset) && $self->{offset} >= $offset && return undef;
        if self.offset >= offset:
            return None
        # my $data;
        data = None
        while self.offset < offset:
            (index, size) = self.r_chunk_open()
            if index == 0 and size == 0:
                self.r_chunk_close()
                # pop @{$self->{end_offsets}}
                self.end_offsets.pop()
                pos = self.offset
                # push @{$self->{end_offsets}}, $pos - 8
                self.end_offsets.append(pos - 8)
                # $offset = $self->{end_offsets}[$#{$self->{end_offsets}}];
                offset = self.end_offsets[-1]
                break
            # last;
            # break

            if index == chunk:
                # push @{$self->{glob_pos}}, $gl_pos;
                self.glob_pos.append(gl_pos)
                return size

            self.r_chunk_close()

        self.offset = gl_pos
        return None

    # }

    def close_found_chunk(self) -> None:
        # my $self = shift;
        offset = self.end_offsets.pop() if self.end_offsets else self.offset
        # defined $offset or $offset = $self->{offset};
        if self.offset <= offset:
            raise ValueError("current position is outside current chunk")
        # $self->{offset} <= $offset or fail('current position is outside current chunk');
        # $self->{offset} = pop @{$self->{glob_pos}};
        self.offset = self.glob_pos.pop()
        # pop @{$self->{start_offsets}};
        self.start_offsets.pop()

    def r_chunk_safe(self, id, dsize) -> int | None:
        # my $self = shift;
        # my ($id, $dsize) = @_;
        size = self.find_chunk(id)
        if size and size == dsize:
            return size
        if size:
            raise ValueError(
                f"size of chunk {id} ({size}) is not match with expected size ({dsize})",
            )
        return None

    # }
    def r_chunk_data(self, size=None):
        # my $self = shift;
        # my ($size) = @_;
        offset = self.end_offsets[-1]  # $self->{end_offsets}[$#{$self->{end_offsets}}];
        # defined($size) or $size = $offset - $self->{offset};
        if size is None:
            size = offset - self.offset
        if offset > self.offset + size:
            raise ValueError(
                "length of requested data is bigger than one left in chunk",
            )
        # $self->{offset} + $size <= $offset or fail('length of requested data is bigger than one left in chunk');
        data = ""
        if size > 0:
            # $data = substr(${$self->{input_data}}, $self->{offset}, $size) or fail('cannot read requested data');
            data = self.input_data[self.offset : self.offset + size]
        self.offset += size
        return data

    def seek(self, seek_offset):
        # my $self = shift;
        # my ($seek_offset) = @_;
        # defined($seek_offset) or fail('you must set seek offset to use this method');
        # my $base = $self->{start_offsets}[$#{$self->{start_offsets}}];
        base = self.start_offsets[-1]
        if self.mode == "w":
            self.fh.seek(base + seek_offset)

        self.offset = base + seek_offset

    def w_chunk_open(self, index: int):
        # my $self = shift;
        # my ($index) = @_;
        data = pack("VV", index, 0xAAAAAAAA)
        if self.mode == "data":
            self.output_data += data
        elif self.mode == "w":
            self.fh.write(data)  # or fail("cannot open chunk $index");
        else:
            raise ValueError("cannot write data while in read-mode")

        # push @{$self->{start_offsets}}, $self->{offset};
        self.start_offsets.append(self.offset)
        # $self->{offset} += 8;
        self.offset += 8

    def w_chunk_close(self):
        # my $self = shift;
        offset = self.start_offsets.pop()  # pop @{$self->{start_offsets}};
        data = pack("V", self.offset - offset - 8)
        if self.mode == "data":
            # substr($self->{output_data}, $offset + 4, 4, $data);
            self.output_data[offset + 4 : offset + 4 + 4] = data
        elif self.mode == "w":
            self.fh.seek(offset + 4)  # or fail("cannot close chunk");
            self.fh.write(data)  # or fail("cannot write size of chunk");
            self.fh.seek(self.offset)  # or fail("cannot seek current write position");
        else:
            raise ValueError("cannot write data while in read-mode")

    # }

    def w_chunk_data(self, data: bytes):
        # my $self = shift;
        # my ($data) = @_;
        size = len(data)
        if self.mode == "data":
            self.output_data += data
        elif self.mode == "w":
            self.fh.write(data)  # or fail("cannot write data");
        else:
            raise ValueError("cannot write data while in read-mode")

        self.offset += size

    # }
    def w_chunk(self, index: int, data: bytes):
        # my $self = shift;
        # my ($index, $data) = @_;
        size = len(data)
        hdr = pack("VV", index, size)
        if self.mode == "data":
            self.output_data += hdr
            self.output_data += data
        elif self.mode == "w":
            self.fh.write(hdr)  # or fail("cannot write header of chunk $index");
            if size > 0:
                self.fh.write(
                    data,
                )  # raise ValueError("cannot write data in chunk $index")
        else:
            raise ValueError("cannot write data while in read-mode")

        self.offset += size + 8

    # }
    def data(self):
        return self.output_data
